import os
import shutil
from datetime import datetime, timedelta
import time
import math

class StorageManager:
    """
    Gerencia o armazenamento na pasta de vídeos, aplicando políticas de retenção
    (tempo decorrido) e limite de espaço (percentagem de uso do disco).
    """
    
    # Políticas de retenção e espaço
    RETENTION_DAYS = 15
    SPACE_LIMIT_PERCENT = 60.0
    
    # Constante para conversão (1024 * 1024 * 1024)
    GB_SCALE = 1024 ** 3

    def __init__(self, video_path: str, test_total_storage_gb: float = None):
        """
        Inicializa o gerenciador.

        :param video_path: Caminho da pasta de vídeos a ser gerenciada.
        :param test_total_storage_gb: Valor em GB para simular o tamanho total do disco.
                                      Use None para usar o tamanho real do sistema.
        """
        self._video_path = video_path
        self._test_total_storage_gb = test_total_storage_gb
        
        if not os.path.isdir(video_path):
            raise FileNotFoundError(f"O diretório '{video_path}' não existe.")
        
        print(f"Gerenciador inicializado para a pasta: {self._video_path}")
        if self._test_total_storage_gb:
             print(f"ATENÇÃO: Usando espaço total de disco SIMULADO: {self._test_total_storage_gb:.2f} GB")


    def set_test_total_storage_gb(self, size_gb: float):
        """Define o valor para simulação de armazenamento total do sistema."""
        self._test_total_storage_gb = size_gb
        print(f"Modo de teste: Espaço total setado para {size_gb:.2f} GB.")

    # --- Funções Auxiliares de Medição ---

    def _get_system_disk_usage(self):
        """
        Retorna o uso total (efetivo/simulado), usado real e livre do disco.
        No modo de teste, também imprime o total real.
        """
        try:
            # Pega o uso real do disco onde o _video_path reside
            total_real, used_real, free_real = shutil.disk_usage(self._video_path)
            
            total_effective = total_real
            used_effective = used_real # O espaço usado é sempre o real
            free_effective = free_real
            
            # Se o modo de teste estiver ativo, substitui o total pelo valor setado.
            if self._test_total_storage_gb is not None:
                simulated_total = self._test_total_storage_gb * self.GB_SCALE
                
                # O total efetivo para o cálculo de porcentagem é o simulado
                total_effective = simulated_total 
                
                # Recalcula 'free' de forma segura (não é usado para a política de espaço, mas é consistente)
                free_effective = max(0, total_effective - used_real)
                
                # Adiciona a impressão do espaço total REAL, conforme solicitado
                print(f"INFO: Espaço Total REAL do Sistema: {total_real / self.GB_SCALE:.2f} GB")

            # Retorna as métricas efetivas para o cálculo da política de espaço
            return total_effective, used_effective, free_effective

        except Exception as e:
            print(f"Erro ao obter uso do disco: {e}")
            return 0, 0, 0
    
    def _get_video_files(self):
        """Retorna uma lista de caminhos completos dos arquivos .mp4 na pasta."""
        files = []
        for entry in os.scandir(self._video_path):
            # Garante que só pega arquivos de vídeo (mp4, avi, mov)
            if entry.is_file() and entry.name.lower().endswith(('.mp4', '.avi', '.mov')):
                files.append(entry.path)
        return files

    # --- Políticas de Exclusão ---

    def _check_retention_policy(self):
        """Deleta arquivos mais antigos que RETENTION_DAYS."""
        
        cutoff_date = datetime.now() - timedelta(days=self.RETENTION_DAYS)
        deleted_count = 0
        deleted_size = 0
        
        print(f"\n[Política de Retenção] A procurar ficheiros anteriores a {cutoff_date.strftime('%Y-%m-%d')}...")

        for file_path in self._get_video_files():
            try:
                # Usa o tempo de última modificação para determinar a idade
                mod_timestamp = os.path.getmtime(file_path)
                mod_date = datetime.fromtimestamp(mod_timestamp)

                if mod_date < cutoff_date:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_count += 1
                    deleted_size += file_size
                    print(f"  🗑️ Deletado por idade: {os.path.basename(file_path)} (Modificado em: {mod_date.strftime('%Y-%m-%d')})")

            except OSError as e:
                print(f"Erro ao deletar ou processar {file_path}: {e}")

        if deleted_count > 0:
            print(f"✅ Ficheiros antigos removidos: {deleted_count} (Total: {deleted_size / self.GB_SCALE:.2f} GB)")
        else:
            print("Nenhum ficheiro encontrado com mais de 15 dias.")
        
        return deleted_count

    def _check_space_policy(self):
        """Deleta os arquivos mais antigos (após 15 dias) até que o uso de disco caia abaixo do limite."""
        
        total_bytes, used_bytes, _ = self._get_system_disk_usage()
        
        if total_bytes <= 0:
            print("❌ Erro: Não foi possível obter o tamanho total do disco.")
            return 0

        # Calcula o limite em bytes
        limit_bytes = (total_bytes * self.SPACE_LIMIT_PERCENT) / 100
        current_usage_percent = (used_bytes / total_bytes) * 100
        
        print(f"\n[Política de Espaço] Uso Atual do Disco: {current_usage_percent:.2f}% (Limite: {self.SPACE_LIMIT_PERCENT:.2f}%)")
        
        if current_usage_percent < self.SPACE_LIMIT_PERCENT:
            print("Não é necessário liberar espaço.")
            return 0

        # Se o limite foi ultrapassado, começamos a deletar
        print("🚨 LIMITE EXCEDIDO! Iniciando exclusão de ficheiros mais antigos...")
        
        # Obtém todos os ficheiros (agora só os que sobraram da política de retenção)
        all_files = self._get_video_files()
        
        # Ordena pelo tempo de modificação (do mais antigo para o mais novo)
        files_to_delete_sorted = sorted(
            [(os.path.getmtime(f), f) for f in all_files],
            key=lambda x: x[0]
        )
        
        bytes_freed = 0
        
        # Continua a deletar até que o espaço usado (o numerador na porcentagem) seja inferior ao limite
        # Nota: Idealmente, o 'used_bytes' aqui deveria ser o espaço total da pasta de vídeos, 
        # mas mantive o 'used' do disco para aderir ao pedido de "armazenamento total do sistema".
        while current_usage_percent >= self.SPACE_LIMIT_PERCENT and files_to_delete_sorted:
            
            # Pega o ficheiro mais antigo na lista (o elemento 1 é o path)
            oldest_file_path = files_to_delete_sorted.pop(0)[1]
            
            try:
                file_size = os.path.getsize(oldest_file_path)
                os.remove(oldest_file_path)
                
                # Atualiza o uso de bytes (assumindo que o espaço liberado afeta o 'used_bytes')
                used_bytes -= file_size
                bytes_freed += file_size
                
                # Recalcula o percentual de uso para verificar a condição de saída do loop
                current_usage_percent = (used_bytes / total_bytes) * 100
                
                print(f"  🗑️ Deletado por limite de espaço: {os.path.basename(oldest_file_path)} (Uso Atual: {current_usage_percent:.2f}%)")
                
            except OSError as e:
                print(f"Erro ao deletar {oldest_file_path} durante a limpeza de espaço: {e}")
        
        # Verifica o uso final
        print(f"✅ Espaço libertado: {bytes_freed / self.GB_SCALE:.2f} GB.")
        print(f"Uso Final do Disco: {current_usage_percent:.2f}%")

        return bytes_freed

    # --- Método Principal de Gerenciamento ---

    def manage_storage(self):
        """
        Executa as duas políticas de exclusão em ordem:
        1. Política de Retenção (15 dias).
        2. Política de Espaço (60% do disco).
        """
        print("\n==============================================")
        print(f"Iniciando Gerenciamento de Armazenamento - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("==============================================")
        
        # 1. Política de Retenção (remove ficheiros antigos)
        self._check_retention_policy()
        
        # 2. Política de Espaço (remove os mais antigos para liberar espaço, se necessário)
        self._check_space_policy()
        
        print("\nGerenciamento de Armazenamento Concluído.")


# --- EXEMPLO DE USO ---
if __name__ == '__main__':
    
    # ⚠️ IMPORTANTE: Substitua pelo caminho real para a sua pasta de vídeos
    TEST_DIR = os.path.join(os.getcwd(), "test_videos") 
    
    # Cria o diretório de teste se ele não existir
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
        print(f"Diretório de teste criado: {TEST_DIR}")
    
    # --- SIMULAÇÃO DE ARQUIVOS ---
    def create_dummy_file(filename, age_days, size_mb=10):
        """Cria um arquivo dummy e define seu tempo de modificação."""
        path = os.path.join(TEST_DIR, filename)
        
        # Cria um arquivo de preenchimento (apenas se não existir)
        if not os.path.exists(path):
             with open(path, 'wb') as f:
                # Cria um arquivo com o tamanho especificado (em bytes)
                f.write(os.urandom(size_mb * 1024 * 1024)) 
        
        # Define o tempo de modificação para simular a idade
        mod_time = time.time() - (age_days * 24 * 60 * 60)
        os.utime(path, (mod_time, mod_time))
        print(f"Criado {filename} ({size_mb}MB), Idade: {age_days} dias.")
        return path

    print("\n--- Preparando arquivos de teste ---")
    
    # Arquivos que serão criados (ou terão a data de modificação atualizada)
    
    # Ficheiro 1: Antigo (será deletado pela Política de Retenção)
    create_dummy_file("video_a_antigo_1.mp4", 20, 50) 
    
    # Ficheiros 2, 3, 4: Recentes (< 15 dias). O total do tamanho desses ficheiros (250MB) 
    # será somado ao uso real do seu disco e comparado ao disco simulado de 1GB (Limite: 600MB).
    # O total real do disco é usado como o 'used_bytes', então se o seu disco real tiver 
    # muito espaço usado, ele forçará a exclusão.

    # ⚠️ PARA TESTAR A POLÍTICA DE ESPAÇO:
    # A política de espaço só atua em ficheiros que SOBREVIVERAM à política de retenção.
    # Vamos criar um ficheiro GRANDE e recente para garantir que o limite de 60%
    # seja atingido (ou ultrapassado) na sua simulação.
    
    # Ficheiro GRANDE, recente, que será o primeiro a ser deletado pela política de espaço
    create_dummy_file("video_z_velho_espaco.mp4", 10, 100) # Terá 10 dias - Sobrevive
    
    # Ficheiro RECENTE (não será deletado)
    create_dummy_file("video_c_recente_3.mp4", 5, 20) # Terá 5 dias - Sobrevive
    
    # Ficheiro EXTRA ANTIGO (será deletado pela Política de Retenção)
    create_dummy_file("video_d_muito_antigo_4.avi", 50, 80) 

    # --- INICIALIZAÇÃO E TESTE ---
    
    # Inicializa o gerenciador. Usaremos o modo de teste para forçar o limite.
    # Simula um disco de 1 GB (1024 MB). Limite de 60% = 614.4 MB.
    # ATENÇÃO: Se o seu disco físico real já tiver um uso elevado, a simulação 
    # forçará a exclusão para tentar atingir os 60% do disco simulado.
    storage_mgr = StorageManager(
        video_path=TEST_DIR, 
        test_total_storage_gb=1.0 # Simulação de disco de 1 GB
    )
    
    # Execute a gestão de armazenamento
    storage_mgr.manage_storage()

    # --- Teste de Limpeza ---
    print("\n--- Verificando ficheiros restantes ---")
    remaining_files = os.listdir(TEST_DIR)
    if remaining_files:
        for f in remaining_files:
            # O getmtime retorna o tempo em segundos desde a "epoch"
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(TEST_DIR, f)))
            print(f"  Ficheiro restante: {f} (Modificado em: {mod_time.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("Nenhum ficheiro restante na pasta de teste.")