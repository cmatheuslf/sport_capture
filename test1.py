import cv2
frame = 30
stime = 15
window_width = frame * stime

array  = [[0]] * window_width
i =0
j = 0

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
    

    #guarda os frames dos 15 segundos anteriores
    i = (i%window_width)
    if(j==0):
        array[i] = frame
        print(frame)
    else:
        array = array[1:window_width] + [frame.copy()] #trocar input por função de captura de frame
    i = i+1
    if(i >= window_width):
         j=1
    # Mostra o frame (opcional, pode remover em uso headless)
    cv2.imshow('gravando', frame)
    signal = cv2.waitKey(1) & 0xFF
    # Pressione 'q' para sair
    if signal == ord('q'):
        break
    if signal == ord('r'):
        print(len(array))
        

        for count in range(window_width):
            print(type(array[count]))
            print(array[count].shape)
            out.write(array[count])
# Libera tudo ao final
cap.release()
out.release()
cv2.destroyAllWindows()

