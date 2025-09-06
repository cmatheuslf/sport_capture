import cv2

# Inicializa a captura de vídeo (0 = primeira câmera conectada)
cap = cv2.VideoCapture(0)

# Define o codec e cria o objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'H264')  # ou 'MJPG', 'X264'
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

# Verifica se a câmera abriu corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

print("Gravando... Pressione 'q' para parar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame.")
        break

    # Escreve o frame no arquivo de vídeo
    out.write(frame)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS do vídeo: {fps}")

    # Mostra o frame (opcional, pode remover em uso headless)
    cv2.imshow('Gravando', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera tudo ao final
cap.release()
out.release()
cv2.destroyAllWindows()
