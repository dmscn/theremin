import cv2

def list_available_cameras(max_tested=5):
    """Lista todas as câmeras disponíveis no sistema."""
    available_cameras = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

print("Buscando câmeras disponíveis...")
cameras = list_available_cameras()
print(f"Câmeras disponíveis: {cameras}")

if not cameras:
    print("Nenhuma câmera encontrada.")
else:
    print(f"Testando a câmera {cameras[0]}...")
    cap = cv2.VideoCapture(cameras[0])
    
    if not cap.isOpened():
        print("Não foi possível abrir a câmera.")
    else:
        print("Câmera aberta com sucesso! Pressione 'q' para sair.")
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Erro ao capturar o frame.")
                    break
                cv2.imshow('Webcam', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            print("\nEncerrando pelo usuário...")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("Recursos liberados.")

if __name__ == "__main__":
    pass
