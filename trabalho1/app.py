# Importações
from flask import Flask, render_template, request
from PIL import Image
import os
import filtros

# Cria a aplicação Flask
app = Flask(__name__)
# Define as pastas para upload e imagens processadas
UPLOAD_FOLDER = 'static/uploads'
PROCESSED_FOLDER = 'static/processed'

# Cria essas pastas caso ainda não existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Define a rota principal da aplicação, aceita GET e POST
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        filtro_nome = request.form.get('filtro') # Obtém o nome do filtro escolhido no formulário
        file = request.files['imagem'] # Obtém o arquivo de imagem enviado
        # Verifica se o arquivo foi enviado e tem extensão válida
        if file and file.filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(UPLOAD_FOLDER, file.filename) # Salva o caminho da imagem original
            file.save(img_path) # Salva a imagem original na pasta de uploads
            img = Image.open(img_path) # Abre a imagem com PIL

            # Dicionário que associa os nomes dos filtros com as funções definidas no módulo 'filtros'
            filtros_disponiveis = {
                'negativo': filtros.filtro_negativo,
                'escala_cinza': filtros.filtro_escala_cinza,
                'contorno': filtros.filtro_contorno,
                'gama': filtros.filtro_gama,
                'log': filtros.filtro_logaritmo,
                'pb': filtros.filtro_pb,
                'blur': filtros.filtro_blur,
                'sharpen': filtros.filtro_sharpen,
                'sobel': filtros.filtro_sobel,
                'laplaciano': filtros.filtro_laplaciano,
                'piwwit': filtros.filtro_piwwit,
                'ruido': filtros.filtro_ruido
            }

            # Seleciona a função do filtro com base na escolha do usuário
            func_filtro = filtros_disponiveis.get(filtro_nome, lambda x: x)
            img_processada = func_filtro(img) # Aplica o filtro à imagem

            # Define o caminho onde a imagem processada será salva
            processed_path = os.path.join(PROCESSED_FOLDER, file.filename)
            img_processada.save(processed_path) # Salva a imagem com o filtro aplicado
            
            # Renderiza o template e passa os caminhos das imagens e o filtro usado
            return render_template(
                'index.html',
                original=img_path,
                processada=processed_path,
                filtro = filtro_nome
            )

    return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True) # Inicia o servidor Flask (por padrão, roda em localhost:5000)