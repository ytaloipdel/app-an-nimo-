import os
from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "uma-chave-muito-secreta-aqui" # Isso protege a sessão

# Dados de acesso (Depois podemos colocar isso num banco de dados)
USUARIO_ADM = "admin"
SENHA_ADM = "empresa123"
ARQUIVO_TXT = "mensagens.txt"

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def receber_mensagem():
    msg = request.form.get('conteudo')
    if msg:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open(ARQUIVO_TXT, "a+", encoding="utf-8") as arquivo:
            arquivo.write(f"[{agora}] {msg}\n")
    return "<h1>Enviado com anonimato!</h1><br><a href='/'>Voltar</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        
        if usuario == USUARIO_ADM and senha == SENHA_ADM:
            session['logado'] = True
            return redirect('/meuapp')
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos!")
    
    return render_template('login.html')

@app.route('/meuapp')
def ver_mensagens():
    # Verifica se o "crachá" de logado existe na sessão
    if not session.get('logado'):
        return redirect('/login')

    lista = []
    if os.path.exists(ARQUIVO_TXT):
        with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:
            lista = arquivo.readlines()
    
    return render_template('adm.html', mensagens=lista)

@app.route('/sair')
def sair():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
