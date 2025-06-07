"""
hand_detector.py

Responsável por detectar mãos e desenhar landmarks usando MediaPipe Hands.
"""
import mediapipe as mp
import cv2
import numpy as np

class HandDetector:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.6):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=2, circle_radius=3)

    def detect(self, frame: np.ndarray):
        # Converte BGR para RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        return results

    def draw(self, frame: np.ndarray, results) -> np.ndarray:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.drawing_spec,
                    self.drawing_spec
                )
        return frame
