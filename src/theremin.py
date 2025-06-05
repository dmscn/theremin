"""
Módulo de captura de vídeo para o Teremim Invisível.

Fornece a classe CameraCapture para inicialização, captura e liberação de frames de vídeo.

Requisitos: OpenCV, numpy
"""
from typing import Optional
import cv2
import numpy as np

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

# Teste unitário básico
if __name__ == "__main__":
    cam = CameraCapture()
    frame = cam.get_frame()
    assert frame is not None, "Falha ao capturar frame."
    assert frame.shape == (480, 640, 3), f"Formato inesperado: {frame.shape}"
    print("Teste de captura de vídeo OK.")
    cam.release()
