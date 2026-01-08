import os
import matplotlib.pyplot as plt
import numpy as np

def obter_lista_tamanhos(caminho_pasta):
    try:
        itens = os.listdir(caminho_pasta)
        arquivos = [f for f in itens if os.path.isfile(os.path.join(caminho_pasta, f))]
        return [os.path.getsize(os.path.join(caminho_pasta, f)) / (1024 * 1024) for f in arquivos]
    except Exception as e:
        print(f"Erro ao acessar {caminho_pasta}: {e}")
        return []

# --- CONFIGURAÇÃO ---
pastas = {
    "h264": "/home/wisepc/Documentos/sport_capture/Videos/h264",
    "mp4v": "/home/wisepc/Documentos/sport_capture/Videos/mp4v"
}

# --- PROCESSAMENTO ---
dados_h264 = obter_lista_tamanhos(pastas["h264"])
dados_mp4v = obter_lista_tamanhos(pastas["mp4v"])

# Encontrar o range global para equalizar os eixos X
todos_os_tamanhos = dados_h264 + dados_mp4v
if not todos_os_tamanhos:
    print("Nenhum arquivo encontrado.")
    exit()

min_x = min(todos_os_tamanhos)
max_x = max(todos_os_tamanhos)

# Criamos 10 bins (intervalos) fixos baseados no range global
intervalos = np.linspace(min_x, max_x, 11)

# --- CRIAÇÃO DO GRÁFICO ---
# sharex=True garante que o eixo X seja idêntico em ambos
# sharey=True garante que o eixo Y seja idêntico em ambos
fig, eixos = plt.subplots(1, 2, figsize=(15, 6), sharex=True, sharey=True)
fig.suptitle('Análise de Frequência de Tamanho (Mesma Escala X/Y)', fontsize=16)

# Gráfico h264
eixos[0].hist(dados_h264, bins=intervalos, color='skyblue', edgecolor='black', alpha=0.8)
eixos[0].set_title('Codec: h264', fontweight='bold')
eixos[0].set_ylabel('Quantidade de Arquivos')
eixos[0].set_xlabel('Tamanho (MB)')
eixos[0].grid(axis='y', linestyle='--', alpha=0.3)

# Gráfico mp4v
eixos[1].hist(dados_mp4v, bins=intervalos, color='salmon', edgecolor='black', alpha=0.8)
eixos[1].set_title('Codec: mp4v', fontweight='bold')
eixos[1].set_xlabel('Tamanho (MB)')
eixos[1].grid(axis='y', linestyle='--', alpha=0.3)

# Ajuste fino para exibir os valores dos bins no eixo X
plt.xticks(intervalos, rotation=45)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()