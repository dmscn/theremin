import cv2

def main():
    # Inicializa a captura de vídeo da webcam padrão (0)
    cap = cv2.VideoCapture(0)
    
    # Verifica se a webcam foi aberta corretamente
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        return
    
    print("Pressione 'q' para sair...")
    
    while True:
        # Captura frame a frame
        ret, frame = cap.read()
        
        # Se o frame for lido corretamente, ret é True
        if not ret:
            print("Erro: Não foi possível capturar o frame.")
            break
        
        # Exibe o frame resultante
        cv2.imshow('Webcam', frame)
        
        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libera a captura e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
