"""
Módulo de captura de vídeo e processamento de mãos para o Teremim Invisível.

Fornece a classe CameraCapture para inicialização, captura e liberação de frames de vídeo,
e a classe HandProcessor para processamento de gestos das mãos.

Requisitos: OpenCV, numpy, mediapipe
"""
from typing import Optional
import cv2
import numpy as np
import mediapipe as mp
import sounddevice as sd
import threading
import time
import json
import queue
try:
    import psutil
except ImportError:
    psutil = None
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.graphics import Color, Line

class CameraCapture:
    """Classe para captura de vídeo com OpenCV.

    Args:
        device (int): Índice do dispositivo de vídeo (default: 0).
    """
    def __init__(self, device: int = 0):
        self.cap = cv2.VideoCapture(device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 20)

    def get_frame(self) -> Optional[np.ndarray]:
        """Captura um frame da câmera, aplica flip horizontal e converte para RGB.

        Returns:
            Optional[np.ndarray]: Frame no formato (480, 640, 3) RGB ou None se falhar.
        """
        success, frame = self.cap.read()
        if not success or frame is None:
            return None
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return cv2.flip(frame_rgb, 1)

    def release(self) -> None:
        """Libera o recurso da câmera."""
        if self.cap.isOpened():
            self.cap.release()

class HandProcessor:
    """Hand gesture processor using MediaPipe Hands.

    Attributes:
        hands: MediaPipe Hands object.
    """
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process(self, frame: np.ndarray) -> dict:
        """Process an RGB frame and extract hand landmarks and gestures.

        Args:
            frame (np.ndarray): RGB image (480, 640, 3)
        Returns:
            dict: {
                'left_hand': list of 21 (x, y, z) or None,
                'right_hand': list of 21 (x, y, z) or None,
                'gestures': {'left_pinch': bool, 'right_height': float}
            }
        """
        # Batch processing: process only every 2 frames
        if not hasattr(self, '_frame_count'):
            self._frame_count = 0
            self._last_result = None
        self._frame_count += 1
        if self._frame_count % 2 != 0:
            return self._last_result if self._last_result else {
                'left_hand': None, 'right_hand': None, 'gestures': {'left_pinch': False, 'right_height': None}
            }
        results = self.hands.process(frame.astype(np.float32))
        left_hand = None
        right_hand = None
        left_pinch = False
        right_height = None
        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_handedness in enumerate(results.multi_handedness):
                label = hand_handedness.classification[0].label.lower()
                landmarks = results.multi_hand_landmarks[idx].landmark
                coords = [(np.float32(lm.x), np.float32(lm.y), np.float32(lm.z)) for lm in landmarks]
                if label == 'left':
                    left_hand = coords
                    # Pinch: distance between thumb tip (4) and index tip (8)
                    pinch_dist = np.linalg.norm(np.array(coords[4][:2]) - np.array(coords[8][:2]))
                    left_pinch = pinch_dist < 0.07
                elif label == 'right':
                    right_hand = coords
                    # Height: y of wrist (0), invert (top=1.0, bottom=0.0)
                    right_height = 1.0 - coords[0][1]
        self._last_result = {
            'left_hand': left_hand,
            'right_hand': right_hand,
            'gestures': {
                'left_pinch': left_pinch,
                'right_height': right_height
            }
        }
        return self._last_result

class SoundGenerator:
    """Real-time sound synthesis using SoundDevice (square wave, buffer 512 samples).

    Attributes:
        sample_rate (int): Audio sample rate (Hz).
        buffer_size (int): Buffer size in samples.
        frequency (float): Base frequency (Hz).
        pitch (float): Pitch multiplier.
        phase (float): Current phase of the oscillator.
        stream (sd.OutputStream): SoundDevice output stream.
        lock (threading.Lock): Thread lock for parameter updates.
    """
    def __init__(self):
        self.sample_rate = 44100
        self.buffer_size = 512
        self.frequency = 440.0
        self.pitch = 1.0
        self.phase = 0.0
        self.stream = None
        self.lock = threading.Lock()
        self.audio_queue = queue.Queue(maxsize=4)
        self._audio_thread = None
        self._running = False
        self._prealloc_buffer = np.zeros((self.buffer_size, 1), dtype=np.float32)

    def audio_callback(self, outdata, frames, time, status):
        """Callback for SoundDevice stream. Generates square wave audio."""
        # Use preallocated buffer and float32
        t = (np.arange(frames, dtype=np.float32) + self.phase) / self.sample_rate
        with self.lock:
            freq = np.float32(self.frequency * self.pitch)
        wave = 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))
        self._prealloc_buffer[:frames, 0] = wave.astype(np.float32)
        outdata[:frames, 0] = self._prealloc_buffer[:frames, 0]
        self.phase = (self.phase + frames) % self.sample_rate

    def update_parameters(self, freq: float, pitch: float) -> None:
        """Update frequency and pitch parameters.

        Args:
            freq (float): Base frequency in Hz.
            pitch (float): Pitch multiplier.
        """
        with self.lock:
            self.frequency = np.clip(freq, 200.0, 2000.0)
            self.pitch = np.clip(pitch, 0.5, 2.0)

    def start_stream(self) -> None:
        """Start the audio output stream."""
        if self.stream is None:
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                blocksize=self.buffer_size,
                channels=1,
                dtype='float32',
                callback=self.audio_callback
            )
            self.stream.start()
            self._running = True
            if self._audio_thread is None:
                self._audio_thread = threading.Thread(target=self._audio_worker, daemon=True)
                self._audio_thread.start()

    def _audio_worker(self):
        while self._running:
            time.sleep(0.01)

    def stop_stream(self) -> None:
        """Stop the audio output stream."""
        self._running = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self._audio_thread = None

class ThereminUI(App):
    """Kivy App for Invisible Theremin with camera preview, frequency label, pitch slider, and hand landmarks overlay."""
    def build(self):
        self.cam = CameraCapture()
        self.hand_proc = HandProcessor()
        self.sound_gen = SoundGenerator()
        self.sound_gen.start_stream()
        self.current_freq = 440.0
        self.current_pitch = 1.0
        self.frame = None
        layout = BoxLayout(orientation='vertical', spacing=10)
        self.image_widget = Image(size_hint_y=0.8)
        self.freq_label = Label(text=f'Frequency: {self.current_freq:.1f} Hz', font_size='20sp', size_hint_y=0.1)
        self.pitch_slider = Slider(min=0.5, max=2.0, value=1.0, step=0.01, size_hint_y=0.1)
        self.pitch_slider.bind(value=self.on_slider_change)
        layout.add_widget(self.image_widget)
        layout.add_widget(self.freq_label)
        layout.add_widget(self.pitch_slider)
        Clock.schedule_interval(self.update, 1.0/20.0)
        return layout

    def on_slider_change(self, instance, value):
        self.current_pitch = value
        self.sound_gen.update_parameters(self.current_freq, self.current_pitch)

    def update(self, dt):
        frame = self.cam.get_frame()
        if frame is None:
            return
        gestures = self.hand_proc.process(frame)
        # Frequency from right hand height
        if gestures['right_hand'] is not None and gestures['gestures']['right_height'] is not None:
            self.current_freq = 200.0 + 1800.0 * np.clip(gestures['gestures']['right_height'], 0.0, 1.0)
        else:
            self.current_freq = 440.0
        # Pitch from slider (UI) or left pinch
        if gestures['left_hand'] is not None:
            if gestures['gestures']['left_pinch']:
                self.current_pitch = 2.0
        self.sound_gen.update_parameters(self.current_freq, self.current_pitch)
        self.freq_label.text = f'Frequency: {self.current_freq:.1f} Hz'
        # Convert frame to Kivy texture
        buf = frame.flatten()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image_widget.texture = texture
        # Draw hand landmarks overlay
        self.image_widget.canvas.after.clear()
        with self.image_widget.canvas.after:
            Color(0, 1, 0, 0.7)
            for hand in ['left_hand', 'right_hand']:
                points = gestures[hand]
                if points:
                    w, h = frame.shape[1], frame.shape[0]
                    for x, y, z in points:
                        px, py = int(x * w), int(y * h)
                        Line(circle=(px, h-py, 4), width=1.5)

    def on_stop(self):
        self.cam.release()
        self.sound_gen.stop_stream()

def main_loop():
    """Main integration loop: video capture, gesture processing, sound synthesis, and performance logging."""
    cam = CameraCapture()
    hand_proc = HandProcessor()
    sound_gen = SoundGenerator()
    sound_gen.start_stream()
    frame_count = 0
    start_time = time.time()
    last_log_time = start_time
    fps = 0.0
    try:
        while True:
            loop_start = time.time()
            frame = cam.get_frame()
            if frame is None:
                print("No camera frame available.")
                time.sleep(0.05)
                continue
            gestures = hand_proc.process(frame)
            freq = 440.0
            pitch = 1.0
            if gestures['right_hand'] is not None and gestures['gestures']['right_height'] is not None:
                freq = 200.0 + 1800.0 * np.clip(gestures['gestures']['right_height'], 0.0, 1.0)
            if gestures['left_hand'] is not None:
                pitch = 2.0 if gestures['gestures']['left_pinch'] else 1.0
            sound_gen.update_parameters(freq, pitch)
            frame_count += 1
            elapsed = time.time() - start_time
            if elapsed > 0:
                fps = frame_count / elapsed
            # Log every 30 frames
            if frame_count % 30 == 0:
                latency_ms = (time.time() - loop_start) * 1000.0
                cpu = psutil.cpu_percent() if psutil else 0.0
                ram = psutil.virtual_memory().used / (1024 * 1024) if psutil else 0.0
                log = {
                    "timestamp": int(time.time()),
                    "fps": round(fps, 2),
                    "latency_ms": round(latency_ms, 2),
                    "cpu_usage": round(cpu, 2),
                    "ram_mb": round(ram, 2)
                }
                print(json.dumps(log))
            # Maintain ~20 FPS
            loop_time = time.time() - loop_start
            sleep_time = max(0, (1.0/20.0) - loop_time)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("Exiting main loop.")
    finally:
        cam.release()
        sound_gen.stop_stream()

# Teste unitário básico
if __name__ == "__main__":
    # Teste da captura de vídeo
    cam = CameraCapture()
    frame = cam.get_frame()
    assert frame is not None, "Falha ao capturar frame."
    assert frame.shape == (480, 640, 3), f"Formato inesperado: {frame.shape}"
    print("Teste de captura de vídeo OK.")
    cam.release()

    # Teste do HandProcessor com uma imagem estática (se disponível)
    import os
    processor = HandProcessor()
    test_img_path = os.path.join(os.path.dirname(__file__), 'hand_sample.jpg')
    if os.path.exists(test_img_path):
        img = cv2.imread(test_img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = processor.process(img_rgb)
        assert 'right_hand' in results, "HandProcessor output missing 'right_hand' key."
        print("HandProcessor static image test OK.")
    
    # Uncomment the line below to run the Kivy UI (requires camera and audio output)
    # ThereminUI().run()
