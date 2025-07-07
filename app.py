# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from backend import bot_aplicar

app = Flask(__name__)
app.config['DADOS_JSON'] = 'dados.json'
app.config['APLICACOES_JSON'] = 'aplicacoes.json'
app.config['JSON_AS_ASCII'] = False

def carregar_dados():
    if os.path.exists(app.config['DADOS_JSON']):
        with open(app.config['DADOS_JSON'], 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
                dados.setdefault('links', {})
                return dados
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_dados(dados):
    with open(app.config['DADOS_JSON'], 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def carregar_aplicacoes():
    if os.path.exists(app.config['APLICACOES_JSON']):
        with open(app.config['APLICACOES_JSON'], 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_aplicacoes(aplicacoes):
    with open(app.config['APLICACOES_JSON'], 'w', encoding='utf-8') as f:
        json.dump(aplicacoes, f, indent=2, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    dados = carregar_dados()
    aplicacoes = carregar_aplicacoes()
    

    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            
            candidatura = {
                "link": link,
                "dados_usuario": dados
            }
            print(candidatura)

            # Chamar bot com candidatura
            resultado = bot_aplicar.bot_aplicar(candidatura)

            aplicacoes.append(resultado)
            salvar_aplicacoes(aplicacoes)
            return redirect(url_for('home'))

    return render_template('home.html', dados=dados, aplicacoes=aplicacoes)


@app.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    dados = carregar_dados()

    if request.method == 'POST':
        dados['nome'] = request.form.get('nome')
        dados['email'] = request.form.get('email')
        dados['telefone'] = request.form.get('telefone')
        dados['password'] = request.form.get('password')
        dados['cpf'] = request.form.get('cpf')

        dados['endereco'] = {
            'rua': request.form.get('rua'),
            'numero': request.form.get('numero'),
            'cidade': request.form.get('cidade'),
            'estado': request.form.get('estado'),
            'cep': request.form.get('cep')
        }

        dados['competencias'] = request.form.get('competencias')

        dados['formacao'] = request.form.get('formacao')

        dados['experiencias'] = request.form.get('experiencias')

        dados['links'] = {
            'linkedin': request.form.get('linkedin'),
            'github': request.form.get('github')
        }

        salvar_dados(dados)
        return redirect(url_for('home'))

    return render_template('editar_perfil.html', dados=dados)

if __name__ == '__main__':
    app.run(debug=True)