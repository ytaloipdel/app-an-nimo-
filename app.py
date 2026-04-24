from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def receber_mensagem():
    msg = request.form.get('conteudo')
    
    # Abrimos o arquivo em modo de "anexar" (append = 'a')
    # O 'utf-8' garante que emojis e acentos funcionem bem
    with open('mensagens.txt', 'a', encoding='utf-8') as f:
        f.write(msg + "\n")
    
    print(f"SALVO NO ARQUIVO: {msg}")
    return "<h1>Mensagem enviada com sucesso!</h1>"

if __name__ == '__main__':
    app.run(debug=True)