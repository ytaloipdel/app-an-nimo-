import os, uuid
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ytalo_solucoes_2026"

# BANCO DE DADOS (Usuário: [Senha, Nome Exibido, Link Atual])
EMPRESAS = {
    "empresa1": {"senha": "123", "nome": "Supermercado Silva", "link_atual": None},
    "empresa2": {"senha": "456", "nome": "Cafeteria Central", "link_atual": None},
    "ytalo_dev": {"senha": "master01", "nome": "Ytalo Soluções Tech", "link_atual": None}
}

@app.route('/')
def home():
    return "<h1>Sistema de Ética</h1><p>Acesse pelo link exclusivo fornecido pela sua empresa.</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('usuario')
        s = request.form.get('senha')
        if u in EMPRESAS and EMPRESAS[u]['senha'] == s:
            session['usuario_logado'] = u
            return redirect(url_for('ver_mensagens'))
    return render_template('login.html')

@app.route('/meuapp')
def ver_mensagens():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario_logado']
    dados = EMPRESAS[usuario]
    arquivo_nome = f"mensagens_{usuario}.txt"
    
    lista = []
    if os.path.exists(arquivo_nome):
        with open(arquivo_nome, "r", encoding="utf-8") as f:
            lista = f.readlines()
            
    return render_template('adm.html', mensagens=lista, nome=dados['nome'], link_convite=dados['link_atual'])

@app.route('/gerar_link')
def gerar_link():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    
    usuario = session['usuario_logado']
    # O Pulo do Gato: Código aleatório único
    novo_codigo = str(uuid.uuid4())[:8] 
    EMPRESAS[usuario]['link_atual'] = novo_codigo
    
    return redirect(url_for('ver_mensagens'))

@app.route('/enviar/<codigo>')
def pagina_envio(codigo):
    id_empresa = None
    for emp, dados in EMPRESAS.items():
        if dados['link_atual'] == codigo:
            id_empresa = emp
            break
            
    if not id_empresa:
        return "<h1>Link inválido ou expirado!</h1>", 404
        
    return render_template('index.html', id_destino=id_empresa, nome=EMPRESAS[id_empresa]['nome'])

@app.route('/processar_envio', methods=['POST'])
def processar_envio():
    destino = request.form.get('id_destino')
    msg = request.form.get('conteudo')
    if msg and destino in EMPRESAS:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open(f"mensagens_{destino}.txt", "a+", encoding="utf-8") as f:
            f.write(f"[{agora}] {msg}\n")
        return "<h1>Enviado com sucesso e anonimato!</h1>"
    return "Erro", 400

@app.route('/sair')
def sair():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
