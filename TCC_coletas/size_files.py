import os
import matplotlib.pyplot as plt

def calcular_tamanho_medio(caminho_pasta):
    try:
        # Lista todos os itens na pasta
        itens = os.listdir(caminho_pasta)
        # Filtra apenas arquivos (ignora subpastas)
        arquivos = [f for f in itens if os.path.isfile(os.path.join(caminho_pasta, f))]
        
        if not arquivos:
            return 0
        
        # Obtém o tamanho de cada arquivo em bytes
        tamanhos = [os.path.getsize(os.path.join(caminho_pasta, f)) for f in arquivos]
        
        # Calcula a média (em Megabytes para facilitar a leitura)
        media_bytes = sum(tamanhos) / len(tamanhos)
        media_mb = media_bytes / (1024 * 1024)
        
        return media_mb
    except Exception as e:
        print(f"Erro ao acessar {caminho_pasta}: {e}")
        return 0

# --- CONFIGURAÇÃO ---
# Substitua pelos caminhos das pastas no seu computador
pastas = {
    "h264": "/home/wisepc/Documentos/sport_capture/Videos/h264",
    #"Pasta 2": "/home/wisepc/Documentos/sport_capture/Videos/avi",
    "mp4v": "/home/wisepc/Documentos/sport_capture/Videos/mp4v"
}

# Processamento
nomes_pastas = list(pastas.keys())
medias = [calcular_tamanho_medio(p) for p in pastas.values()]

# --- CRIAÇÃO DO GRÁFICO ---
plt.figure(figsize=(10, 6))
cores = ['skyblue', 'salmon', 'lightgreen']

barras = plt.bar(nomes_pastas, medias, color=cores)

# Estilização
plt.title('Comparativo de Tamanho Médio dos Arquivos', fontsize=14)
plt.xlabel('Pastas', fontsize=12)
plt.ylabel('Tamanho Médio (MB)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adiciona os valores em cima das barras
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 0.05, f'{yval:.2f} MB', ha='center', va='bottom')

plt.show()