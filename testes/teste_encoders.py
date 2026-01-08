import cv2
import os

def test_codecs():
    # Lista de codecs para testar (FourCC, Extensão)
    codecs = [
        ('mp4v', '.mp4'),  # MPEG-4 (O mais provável de funcionar)
        ('XVID', '.avi'),  # Clássico Linux
        ('MJPG', '.avi'),  # Quase universal
        ('avc1', '.mp4'),  # H.264
        ('vp09', '.avixxxxxxxxxxxxx'), # VP9
    ]
    
    print(f"{'Codec':<10} | {'Ext':<5} | {'Resultado'}")
    print("-" * 30)
    
    for fcc, ext in codecs:
        filename = f"test_{fcc}{ext}"
        fourcc = cv2.VideoWriter_fourcc(*fcc)
        # Tenta criar o arquivo (640x480, 30fps)
        out = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480))
        
        if out.isOpened():
            print(f"{fcc:<10} | {ext:<5} | ✅ FUNCIONA")
            out.release()
            if os.path.exists(filename): os.remove(filename)
        else:
            print(f"{fcc:<10} | {ext:<5} | ❌ FALHOU")

if __name__ == "__main__":
    test_codecs()