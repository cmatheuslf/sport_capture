import os
from flask import Flask, send_from_directory, abort, request, jsonify

# Cria a aplicação Flask
app = Flask(__name__)

# Define o diretório onde os vídeos estão armazenados
# Removi a barra final de 'Videos/' pois o os.path.join lida com isso.
VIDEO_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Videos/')

@app.route('/video/<path:filename>')
def get_video(filename):
    """
    Esta rota serve um arquivo de vídeo do diretório VIDEO_DIR.
    """
    try:
        # send_from_directory lida com a segurança de caminhos
        # e também define o mimetype (tipo de conteúdo) correto.
        
        # Corrigi o print para mostrar o caminho de forma mais clara
        print(f"Tentando servir: {os.path.join(VIDEO_DIR, filename)}")
        
        return send_from_directory(
            VIDEO_DIR,
            filename,
            as_attachment=False  # Define como False para o navegador tentar tocar o vídeo
        )
    except FileNotFoundError:
        # Retorna um erro 404 se o arquivo não for encontrado
        abort(404)

# --- NOVO ENDPOINT ---
@app.route('/videos/list', methods=['GET']) # Alterado para aceitar POST
def list_videos():
    """
    Lista os arquivos de vídeo que estão dentro de um intervalo de tempo,
    usando o nome do arquivo como registro.
    
    Espera um JSON no body do request (opcional):
    {
        "start": "2024-11-09_10-00",
        "end": "2024-11-09_12-00"
    }
    """
    
    # 1. Pega os dados do JSON body
    # Tenta parsear o JSON. Se não houver JSON ou estiver vazio, 
    # data será um dicionário vazio ({}).
    data = request.get_json(silent=True) or {}
    
    start_filter = data.get('start')
    end_filter = data.get('end')
    
    print(f"Buscando arquivos. Início: {start_filter}, Fim: {end_filter}")
    
    filtered_files = []
    
    try:
        # 2. Lista todos os arquivos no diretório de vídeos
        print(VIDEO_DIR)
        all_files = os.listdir(VIDEO_DIR)
        
        for filename in all_files:
            # Garante que estamos olhando apenas para arquivos (ignora pastas)
            if not os.path.isfile(os.path.join(VIDEO_DIR, filename)):
                continue
            
            print(f"Verificando arquivo: {filename}")
            # 3. Aplica os filtros (usa comparação de string simples)
            
            # Se 'start' foi fornecido e o arquivo for "menor" (alfabeticamente), pule.
            if start_filter and filename < start_filter:
                continue
            
            # Se 'end' foi fornecido e o arquivo for "maior" (alfabeticamente), pule.
            if end_filter and filename > end_filter:
                continue
                
            # 4. Se passou nos filtros, adicione à lista
            filtered_files.append(filename)
            
        # 5. Retorna a lista filtrada e ordenada como JSON
        filtered_files.sort()
        return jsonify(filtered_files)
        
    except FileNotFoundError:
        return jsonify({"error": "Diretório 'Videos' não encontrado."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- FIM DO NOVO ENDPOINT ---

if __name__ == '__main__':
    # Roda a aplicação
    # host='0.0.0.0' torna o servidor acessível na sua rede local
    app.run(debug=True, host='0.0.0.0', port=5000)