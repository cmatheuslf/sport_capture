from ..Classes.Recorder import Recorder
import threading

recorder = Recorder("Casa", "127.0.0.1", 480, 640, "/home/wisepc/Documentos/sport_capture/Videos/")

stream_thread = threading.Thread(target=recorder.recording_last_15s)

    # 4. Inicie a thread.
    #    O programa NÃO vai esperar aqui. Ele inicia a thread e continua imediatamente.
# stream_thread.start()
# stream_thread.join()

recorder.streaming_video()
# while True:
#     rec = input('Pode grava?')
#     if(rec == 's'):
#         recorder.recording_last_15s()


print("Programa Principal: A thread foi iniciada e o programa principal continua a ser executado em paralelo.")