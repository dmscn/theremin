"""
main.py

Consome um stream RTMP e exibe o vídeo em tempo real.
"""
import cv2
import numpy as np
from config import RTMP_URL
from hand_detector import HandDetector

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320
FALLBACK_TEXT = "No video connection"


def wrap_text(text, font, font_scale, thickness, max_width):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        (w, _), _ = cv2.getTextSize(test_line, font, font_scale, thickness)
        if w > max_width and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)
    return lines


def show_fallback_window(text: str = "No video connection", retry_callback=None) -> None:
    """Displays a window with a centered message indicating no video connection and allows retry."""
    bg_color = (40, 40, 40)
    img = np.full((WINDOW_HEIGHT, WINDOW_WIDTH, 3), bg_color, dtype=np.uint8)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.0
    thickness = 2
    color = (230, 230, 230)
    max_text_width = WINDOW_WIDTH - 40
    lines = wrap_text(text, font, font_scale, thickness, max_text_width)
    total_height = sum(cv2.getTextSize(line, font, font_scale, thickness)[0][1] for line in lines) + 10 * (len(lines) - 1)
    y = (WINDOW_HEIGHT - total_height) // 2
    for line in lines:
        (w, h), _ = cv2.getTextSize(line, font, font_scale, thickness)
        x = (WINDOW_WIDTH - w) // 2
        cv2.putText(img, line, (x, y + h), font, font_scale, color, thickness, cv2.LINE_AA)
        y += h + 10
    cv2.putText(img, "Pressione 'r' para tentar novamente", (20, WINDOW_HEIGHT - 20), font, 0.6, (180,180,180), 1, cv2.LINE_AA)
    while True:
        cv2.imshow("RTMP Video", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('r') and retry_callback:
            cv2.destroyAllWindows()
            retry_callback()
            break
    cv2.destroyAllWindows()


def main() -> None:
    """Conecta ao endpoint RTMP, detecta mãos e exibe feedback visual. Permite retry em caso de erro."""
    def try_connect():
        print(f"Tentando conectar ao stream RTMP: {RTMP_URL}")
        cap = cv2.VideoCapture(RTMP_URL)
        if not cap.isOpened():
            print(f"[ERRO] Não foi possível conectar ao stream RTMP: {RTMP_URL}")
            show_fallback_window(f"Erro ao conectar ao stream RTMP:\n{RTMP_URL}", retry_callback=try_connect)
            return
        print(f"[OK] Conectado ao stream: {RTMP_URL}")
        detector = HandDetector()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERRO] Falha ao ler frame do stream. Verifique se o vídeo está sendo enviado.")
                show_fallback_window("Falha ao ler frame do stream.\nPressione 'r' para tentar novamente.", retry_callback=try_connect)
                break
            results = detector.detect(frame)
            frame = detector.draw(frame, results)
            cv2.imshow("RTMP Video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    try_connect()


if __name__ == "__main__":
    main()
