import os, uuid
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ytalo_solucoes_2026"

# Simulando um Banco de Dados de Empresas e seus Links Ativos
# Estrutura: "id_da_empresa": {"senha": "...", "nome": "...", "link_atual": "..."}
EMPRESAS = {
    "empresa1": {"senha": "123", "nome": "Supermercado Silva", "link_atual": None},
    "empresa2": {"senha": "456", "nome": "Cafeteria Central", "link_atual": None}
}

@app.route('/')
def home():
    return "<h1>Sistema Protegido</h1><p>Acesse pelo link da sua empresa.</p>"

# PAINEL DA EMPRESA
@app.route('/meuapp')
def ver_mensagens():
    if 'usuario_logado' not in session: return redirect('/login')
    
    usuario = session['usuario_logado']
    dados = EMPRESAS[usuario]
    
    # Lendo as mensagens
    arquivo_nome = f"mensagens_{usuario}.txt"
    lista = []
    if os.path.exists(arquivo_nome):
        with open(arquivo_nome, "r", encoding="utf-8") as f:
            lista = f.readlines()
            
    return render_template('adm.html', mensagens=lista, nome=dados['nome'], link_convite=dados['link_atual'])

# GERADOR DE LINK ÚNICO
@app.route('/gerar_link')
def gerar_link():
    if 'usuario_logado' not in session: return redirect('/login')
    
    usuario = session['usuario_logado']
    # Gera um código aleatório único
    novo_codigo = str(uuid.uuid4())[:8] 
    EMPRESAS[usuario]['link_atual'] = novo_codigo
    
    return redirect('/meuapp')

# ROTA DE ENVIO DINÂMICA (Onde o funcionário clica)
@app.route('/enviar/<codigo>')
def pagina_envio(codigo):
    # Procura qual empresa é dona desse código
    id_empresa = None
    for emp, dados in EMPRESAS.items():
        if dados['link_atual'] == codigo:
            id_empresa = emp
            break
            
    if not id_empresa:
        return "<h1>Este link expirou ou é inválido!</h1>", 404
        
    return render_template('index.html', id_destino=id_empresa, nome=EMPRESAS[id_empresa]['nome'])

# (As outras rotas de login e processar_envio continuam iguais às anteriores)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('usuario'); s = request.form.get('senha')
        if u in EMPRESAS and EMPRESAS[u]['senha'] == s:
            session['usuario_logado'] = u
            return redirect('/meuapp')
    return render_template('login.html')

@app.route('/processar_envio', methods=['POST'])
def processar_envio():
    destino = request.form.get('id_destino')
    msg = request.form.get('conteudo')
    if msg and destino in EMPRESAS:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open(f"mensagens_{destino}.txt", "a+", encoding="utf-8") as f:
            f.write(f"[{agora}] {msg}\n")
        return "<h1>Enviado com sucesso!</h1>"
    return "Erro", 400import os, uuid
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ytalo_solucoes_2026"

# Simulando um Banco de Dados de Empresas e seus Links Ativos
# Estrutura: "id_da_empresa": {"senha": "...", "nome": "...", "link_atual": "..."}
EMPRESAS = {
    "empresa1": {"senha": "123", "nome": "Supermercado Silva", "link_atual": None},
    "empresa2": {"senha": "456", "nome": "Cafeteria Central", "link_atual": None}
}

@app.route('/')
def home():
    return "<h1>Sistema Protegido</h1><p>Acesse pelo link da sua empresa.</p>"

# PAINEL DA EMPRESA
@app.route('/meuapp')
def ver_mensagens():
    if 'usuario_logado' not in session: return redirect('/login')
    
    usuario = session['usuario_logado']
    dados = EMPRESAS[usuario]
    
    # Lendo as mensagens
    arquivo_nome = f"mensagens_{usuario}.txt"
    lista = []
    if os.path.exists(arquivo_nome):
        with open(arquivo_nome, "r", encoding="utf-8") as f:
            lista = f.readlines()
            
    return render_template('adm.html', mensagens=lista, nome=dados['nome'], link_convite=dados['link_atual'])

# GERADOR DE LINK ÚNICO
@app.route('/gerar_link')
def gerar_link():
    if 'usuario_logado' not in session: return redirect('/login')
    
    usuario = session['usuario_logado']
    # Gera um código aleatório único
    novo_codigo = str(uuid.uuid4())[:8] 
    EMPRESAS[usuario]['link_atual'] = novo_codigo
    
    return redirect('/meuapp')

# ROTA DE ENVIO DINÂMICA (Onde o funcionário clica)
@app.route('/enviar/<codigo>')
def pagina_envio(codigo):
    # Procura qual empresa é dona desse código
    id_empresa = None
    for emp, dados in EMPRESAS.items():
        if dados['link_atual'] == codigo:
            id_empresa = emp
            break
            
    if not id_empresa:
        return "<h1>Este link expirou ou é inválido!</h1>", 404
        
    return render_template('index.html', id_destino=id_empresa, nome=EMPRESAS[id_empresa]['nome'])

# (As outras rotas de login e processar_envio continuam iguais às anteriores)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('usuario'); s = request.form.get('senha')
        if u in EMPRESAS and EMPRESAS[u]['senha'] == s:
            session['usuario_logado'] = u
            return redirect('/meuapp')
    return render_template('login.html')

@app.route('/processar_envio', methods=['POST'])
def processar_envio():
    destino = request.form.get('id_destino')
    msg = request.form.get('conteudo')
    if msg and destino in EMPRESAS:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        with open(f"mensagens_{destino}.txt", "a+", encoding="utf-8") as f:
            f.write(f"[{agora}] {msg}\n")
        return "<h1>Enviado com sucesso!</h1>"
    return "Erro", 400
