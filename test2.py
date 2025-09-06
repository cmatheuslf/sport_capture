import cv2
import subprocess
import numpy as np

frame_rate = 30
save_time = 15
window_width = frame_rate * save_time

array = [[0]] * window_width
i = 0
j = 0

# Tamanho do frame
width = 640
height = 480

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, frame_rate)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

# Inicializa o processo do ffmpeg
ffmpeg_cmd = [
    'ffmpeg',
    '-y',                         # overwrite output file if it exists
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', f'{width}x{height}',
    '-r', str(frame_rate),
    '-i', '-',                   # input from stdin
    '-an',                       # no audio
    '-vcodec', 'libx264',
    '-preset', 'ultrafast',
    '-pix_fmt', 'yuv420p',
    'output.mp4'
]

ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

print("Gravando... Pressione 'q' para parar.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame.")
        break

    # Envia o frame para o FFmpeg via stdin
    ffmpeg_process.stdin.write(frame.tobytes())

    # Guarda os frames dos 15 segundos anteriores
    i = i % window_width
    if j == 0:
        array[i] = frame
    else:
        array = array[1:window_width] + [frame]
    print('array:', i, '\n', array, '\n')
    i += 1
    if i >= window_width:
        j = 1

    # Exibe o frame com FPS aproximado
    text = f'fps: {frame_rate}'
    cv2.imshow(text, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza
cap.release()
ffmpeg_process.stdin.close()
ffmpeg_process.wait()
cv2.destroyAllWindows()
