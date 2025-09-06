import cv2
import threading
from collections import deque
from datetime import datetime 

# Parâmetros do vídeo
frame = 30  # FPS
stime = 15  # Tempo de buffer em segundos
window_width = frame * stime # Número de frames no buffer
 
# Variáveis de controle
record = False
recording_started = False
out = None
buffer_frames = deque(maxlen=window_width)

try:
    # Inicializa a captura de vídeo (0 = primeira câmera conectada)
    cap = cv2.VideoCapture(0)

    # Define o codec e o objeto VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'avc1') # avc1 = h264
    # Note: o VideoWriter deve ser criado apenas quando a gravação começar
    # para garantir que o arquivo seja aberto e fechado corretamente.
    # out = cv2.VideoWriter('output.mp4', fourcc, float(frame), (640, 480))

    # Verifica se a câmera abriu corretamente
    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        exit()

    print("Pronto para gravar... Pressione 'r' para começar a gravar os últimos 15 segundos.")
    print("Pressione 'q' para sair.")

    while True:
        ret, current_frame = cap.read()
        if not ret:
            print("Erro ao capturar frame.")
            break

        # Adiciona o frame atual ao buffer de frames
        buffer_frames.append(current_frame.copy())
        
        # Mostra o frame (opcional, pode remover)
        cv2.imshow("Captura", current_frame)
        
        # Verifica a entrada do usuário
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('r'):
                print("Iniciando gravação...")
                title = datetime.now().strftime("%d_%m_%Y_%H_%M_%S.mp4")
                
                # Cria o objeto VideoWriter aqui
                out = cv2.VideoWriter(title, fourcc, float(frame), (640, 480))
                
                # Grava os frames do buffer no arquivo
                for buffered_frame in buffer_frames:
                    out.write(buffered_frame)
                out.release()
except Exception as e:
    print("Erro: ", e)            
finally:            
    # Libera os recursos
    cap.release()    
    cv2.destroyAllWindows()