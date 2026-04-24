from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Essa é a senha que você vai usar no link para entrar no seu app
SENHA_ADMIN = "ytalo123"

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def receber_mensagem():
    msg = request.form.get('conteudo')
    if msg:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open("mensagens.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{agora}] {msg}\n")
    return "<h1>Enviado com sucesso!</h1><br><a href='/'>Voltar</a>"

# --- SEU APP PARA RECEBER AS MENSAGENS ---
@app.route('/meuapp')
def ver_mensagens():
    senha = request.args.get('senha')
    
    if senha != SENHA_ADMIN:
        return "<h1>Acesso negado!</h1>", 403

    lista = []
    try:
        with open("mensagens.txt", "r", encoding="utf-8") as arquivo:
            lista = arquivo.readlines()
    except:
        lista = ["Nenhuma mensagem ainda."]

    return render_template('adm.html', mensagens=lista)

if __name__ == '__main__':
    app.run(debug=True)