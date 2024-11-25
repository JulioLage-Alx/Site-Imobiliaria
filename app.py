from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from validador import validar_cep, validar_cpf, validar_telefone, validar_valor, validar_data

app = Flask(__name__)

# Configuração do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Julio1975$",  # Substitua com sua senha
    database="imobiliaria"
)

# Secret key para sessão
app.secret_key = '001'

# Rota para a página inicial
@app.route('/')
def home():
    # Renderiza o template index.html
    return render_template('index.html')

# Rota para adicionar imóvel
@app.route('/add_imovel', methods=["GET", "POST"])
def add_imovel():
    if request.method == "POST":
        endereco = request.form['endereco']
        cep = request.form['cep']
        valor_aluguel = request.form['valor_aluguel']
        nome_proprietario = request.form['nome_proprietario']

        # Validações
        if not endereco:
            flash("O endereço é obrigatório.")
            return redirect('/add_imovel')
        if not validar_cep(cep):
            flash("O CEP deve conter exatamente 8 dígitos numéricos.")
            return redirect('/add_imovel')
        if not validar_valor(valor_aluguel):
            flash("O valor do aluguel deve ser um número positivo.")
            return redirect('/add_imovel')
        if not nome_proprietario:
            flash("O nome do proprietário é obrigatório.")
            return redirect('/add_imovel')

        # Inserir no banco de dados
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO imovel (endereco, cep, valor_aluguel, nome_proprietario)
            VALUES (%s, %s, %s, %s)
        """, (endereco, cep, valor_aluguel, nome_proprietario))
        db.commit()

        flash("Imóvel adicionado com sucesso!")
        return redirect('/')

    return render_template('imovel.html')  # Formulário para adicionar imóvel

# Rota para adicionar inquilino
@app.route('/add_inquilino', methods=["GET", "POST"])
def add_inquilino():
    if request.method == "POST":
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento']
        imovel_id = request.form['imovel_id']

        # Validações
        if not nome:
            flash("O nome completo é obrigatório.")
            return redirect('/add_inquilino')
        if not validar_cpf(cpf):
            flash("O CPF deve conter exatamente 11 dígitos numéricos.")
            return redirect('/add_inquilino')
        if not validar_telefone(telefone):
            flash("O telefone deve conter 10 ou 11 dígitos numéricos.")
            return redirect('/add_inquilino')
        if not validar_data(data_nascimento):
            flash("A data de nascimento deve estar no formato AAAA-MM-DD.")
            return redirect('/add_inquilino')
        if not imovel_id:
            flash("É necessário selecionar um imóvel.")
            return redirect('/add_inquilino')

        # Inserir no banco de dados
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO inquilino (nome, cpf, telefone, data_nascimento, imovel_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, cpf, telefone, data_nascimento, imovel_id))
        db.commit()

        flash("Inquilino adicionado com sucesso!")
        return redirect('/')

    # Buscar imóveis para exibir no formulário de inquilino
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, endereco FROM imovel")
    imoveis = cursor.fetchall()

    return render_template('inquilino.html', imoveis=imoveis)  # Formulário para adicionar inquilino

if __name__ == '__main__':
    app.run(debug=True)
