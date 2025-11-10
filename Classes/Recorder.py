import cv2
from collections import deque
from datetime import datetime 

class Recorder:
    # O método construtor agora inicializa os atributos privados.
    # Usamos o sublinhado (_) para indicar que são para uso interno da classe.
    # Parâmetros do vídeo
    frame = 30  # FPS
    stime = 15  # Tempo de buffer em segundos
    window_width = frame * stime # Número de frames no buffer
    
    # Variáveis de controle
    record = False
    recording_started = False
    out = None
    buffer_frames = deque(maxlen=window_width)
    
    def __init__(self, location: str, ip_address: str, cam_height: int, cam_width: int, path: str):
        self._location = location
        self._ip_address = ip_address
        self._cam_height = cam_height
        self._cam_width = cam_width
        self._path = path
        # Corrigindo o f-string para a mensagem de criação
        print(f"Um {self.__class__.__name__} foi criado na localização: {self._location}!")

    # --- Métodos GET (Acessores) ---
    # Usados para ler o valor dos atributos privados.

    def get_location(self):
        """Retorna a localização do gravador."""
        return self._location

    def get_ip_address(self):
        """Retorna o endereço IP do gravador."""
        return self._ip_address

    def get_cam_height(self):
        """Retorna a altura da câmera em pixels."""
        return self._cam_height

    def get_cam_width(self):
        """Retorna a largura da câmera em pixels."""
        return self._cam_width

    # --- Métodos SET (Modificadores) ---
    # Usados para alterar o valor dos atributos privados, com validação.

    def set_location(self, new_location):
        """Define uma nova localização, verificando se é uma string não vazia."""
        if isinstance(new_location, str) and len(new_location) > 0:
            self._location = new_location
        else:
            print("Erro: A localização deve ser um texto não vazio.")

    def set_ip_address(self, new_ip_address):
        """Define um novo endereço IP, verificando se é uma string."""
        # Uma validação real de IP seria mais complexa, mas isto é um exemplo.
        if isinstance(new_ip_address, str):
            self._ip_address = new_ip_address
        else:
            print("Erro: O endereço IP deve ser um texto.")

    def set_cam_height(self, new_height):
        """Define uma nova altura da câmera, verificando se é um número inteiro positivo."""
        if isinstance(new_height, int) and new_height > 0:
            self._cam_height = new_height
        else:
            print("Erro: A altura deve ser um número inteiro maior que zero.")

    def set_cam_width(self, new_width):
        """Define uma nova largura da câmera, verificando se é um número inteiro positivo."""
        if isinstance(new_width, int) and new_width > 0:
            self._cam_width = new_width
        else:
            print("Erro: A largura deve ser um número inteiro maior que zero.")

    # Captura de Vídeo
    def streaming_video(self):
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
                self.buffer_frames.append(current_frame.copy())
                
                # Mostra o frame (opcional, pode remover)
                cv2.imshow("Captura", current_frame)
                
                # Verifica a entrada do usuário
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('r'):
                        print("Iniciando gravação...")
                        title = datetime.now().strftime("%d_%m_%Y_%H_%M_%S.mp4")
                        
                        # Cria o objeto VideoWriter aqui
                        out = cv2.VideoWriter(title, fourcc, float(self.frame), (self.get_cam_width(), self.get_cam_height()))
                        
                        
                        # Grava os frames do buffer no arquivo
                        for buffered_frame in self.buffer_frames:
                            out.write(buffered_frame)
                        
                        out.release()
        except Exception as e:
            print("Erro: ", e)            
        finally:            
            # Libera os recursos
            cap.release()    
            cv2.destroyAllWindows()

    #função que o botao de interrupção externa vai apontar para gravar
    def recording_last_15s(self):
        print("Iniciando gravação...")
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        title = self.path+datetime.now().strftime("%d_%m_%Y_%H_%M_%S.mp4")
        
        # Cria o objeto VideoWriter aqui
        out = cv2.VideoWriter(title, fourcc, float(self.frame), (self._cam_width, self._cam_height))
        
        # Grava os frames do buffer no arquivo
        for buffered_frame in self.buffer_frames:
            out.write(buffered_frame)
        out.release()
    # 4. Métodos da Instância
    # São funções que pertencem a um objeto. Eles podem acessar e modificar
    # os atributos da instância (usando 'self').
    def meu_metodo(self):
        print(f"Executando um método para o objeto com o valor: {self.parametro1}")
        return f"O valor do parametro2 é {self.parametro2}"

    # 5. Método de Classe (Opcional)
    # É um método que opera na classe em si, e não na instância.
    # Usa o decorador @classmethod e recebe 'cls' como primeiro argumento.


    # 6. Método Estático (Opcional)
    # É uma função que está dentro da classe, mas não tem acesso nem à classe ('cls')
    # nem à instância ('self'). Funciona como uma função normal, mas pertence ao escopo da classe.
    @staticmethod
    def metodo_estatico(a, b):
        return a + b