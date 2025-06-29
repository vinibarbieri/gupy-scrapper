# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['DADOS_JSON'] = 'dados.json'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def carregar_dados():
    if os.path.exists(app.config['DADOS_JSON']):
        with open(app.config['DADOS_JSON'], 'r') as f:
            try:
                dados = json.load(f)
                dados.setdefault('endereco', {})
                dados.setdefault('formacao', {})
                dados.setdefault('experiencias', [])
                dados.setdefault('links', {})
                return dados
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_dados(dados):
    with open(app.config['DADOS_JSON'], 'w') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

@app.route('/')
def home():
    dados = carregar_dados()
    return render_template('home.html', dados=dados)

@app.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    dados = carregar_dados()

    if request.method == 'POST':
        dados['nome'] = request.form.get('nome')
        dados['email'] = request.form.get('email')
        dados['telefone'] = request.form.get('telefone')
        dados['cpf'] = request.form.get('cpf')

        dados['endereco'] = {
            'rua': request.form.get('rua'),
            'numero': request.form.get('numero'),
            'cidade': request.form.get('cidade'),
            'estado': request.form.get('estado'),
            'cep': request.form.get('cep')
        }

        dados['formacao'] = {
            'curso': request.form.get('curso'),
            'instituicao': request.form.get('instituicao'),
            'ano_inicio': request.form.get('ano_inicio'),
            'ano_fim': request.form.get('ano_fim')
        }

        dados['experiencias'] = [{
            'cargo': request.form.get('cargo'),
            'empresa': request.form.get('empresa'),
            'inicio': request.form.get('inicio'),
            'fim': request.form.get('fim'),
            'descricao': request.form.get('descricao')
        }]

        dados['links'] = {
            'linkedin': request.form.get('linkedin'),
            'github': request.form.get('github')
        }

        if 'curriculo' in request.files:
            file = request.files['curriculo']
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                dados['curriculo_pdf'] = filename

        salvar_dados(dados)
        return redirect(url_for('home'))

    return render_template('editar_perfil.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)