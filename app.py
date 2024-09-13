from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup

app = Flask(__name__)

# Função para remover as tags
def remove_tags(html_content, tag_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(tag_name):
        tag.decompose()  # Remove a tag e o conteúdo
    return str(soup)

# Rota principal (carrega o formulário de upload)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar o upload e a remoção de tags
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo foi enviado', 400
    
    file = request.files['file']
    tag_name = request.form['tag_name']
    
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400
    
    if file:
        html_content = file.read().decode('utf-8')
        html_modificado = remove_tags(html_content, tag_name)
        
        output_filename = 'output.html'
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_modificado)
        
        return send_file(output_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
