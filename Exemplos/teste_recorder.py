from ..Classes.Recorder import Recorder
import threading
import os


recorder = Recorder("Casa", "127.0.0.1", 480, 640, "/home/wisepc/Documentos/sport_capture/Videos/av1/")

#stream_thread = threading.Thread(target=recorder.recording_last_15s)

    # 4. Inicie a thread.
    #    O programa NÃO vai esperar aqui. Ele inicia a thread e continua imediatamente.
# stream_thread.start()
# stream_thread.join()

#recorder.streaming_video('avc1', '.mp4')# ex: 'avc1', '.mp4' para h264 mp4

recorder.streaming_video('AV01', '.mkv')# ex: 'hvc1', '.mp4' para h265 mp4 verificar forma de meljhorar a velocidade

#recorder.streaming_video('mp4v', '.mp4')# ex: 'VP09 ', '.webm' para VP9 webm

# while True:
#     rec = input('Pode grava?')
#     if(rec == 's'):
#         recorder.recording_last_15s()


print("Programa Principal: A thread foi iniciada e o programa principal continua a ser executado em paralelo.")