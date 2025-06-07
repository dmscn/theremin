"""
main.py

Consome um stream RTMP e exibe o vídeo em tempo real.
"""
import cv2
import numpy as np
from config import RTMP_URL

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320
FALLBACK_TEXT = "No video connection"


def show_fallback_window(text: str = "No video connection") -> None:
    """Displays a window with a centered message indicating no video connection."""
    bg_color = (40, 40, 40)
    img = np.full((WINDOW_HEIGHT, WINDOW_WIDTH, 3), bg_color, dtype=np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.0
    thickness = 2
    color = (230, 230, 230)
    line1 = "No video"
    line2 = "connection"
    (w1, h1), _ = cv2.getTextSize(line1, font, font_scale, thickness)
    (w2, h2), _ = cv2.getTextSize(line2, font, font_scale, thickness)
    total_height = h1 + h2 + 10
    y1 = (WINDOW_HEIGHT - total_height) // 2 + h1
    y2 = y1 + h2 + 10
    x1 = (WINDOW_WIDTH - w1) // 2
    x2 = (WINDOW_WIDTH - w2) // 2
    cv2.putText(img, line1, (x1, y1), font, font_scale, color, thickness, cv2.LINE_AA)
    cv2.putText(img, line2, (x2, y2), font, font_scale, color, thickness, cv2.LINE_AA)
    while True:
        cv2.imshow("RTMP Video", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def main() -> None:
    """Conecta ao endpoint RTMP e exibe o vídeo em tempo real ou fallback."""
    cap = cv2.VideoCapture(RTMP_URL)
    if not cap.isOpened():
        print(f"Erro ao conectar ao stream RTMP: {RTMP_URL}")
        show_fallback_window()
        return
    print(f"Conectado ao stream: {RTMP_URL}")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao ler frame do stream.")
            show_fallback_window()
            break
        cv2.imshow("RTMP Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
