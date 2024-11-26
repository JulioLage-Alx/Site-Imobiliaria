from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from validador import validar_cep, validar_cpf, validar_telefone, validar_valor, validar_data

app = Flask(__name__)

# Configuração do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Julio1975$",  
    database="imobiliaria"
)

# Verificar a conexão com o banco de dados
if db.is_connected():
    print("Conexão com o banco de dados bem-sucedida!")
else:
    print("Erro na conexão com o banco de dados!")

# Secret key para sessão
app.secret_key = '001'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_imovel', methods=["GET", "POST"])
def add_imovel():
    if request.method == "POST":
        # Captura os campos do formulário
        cidade = request.form.get('cidade', '').strip()
        numero = request.form.get('numero', '').strip()
        rua = request.form.get('rua', '').strip()
        complemento = request.form.get('complemento', '').strip()
        cep = request.form.get('cep', '').strip()
        valor_aluguel = request.form.get('valor_aluguel', '').strip()
        nome_proprietario = request.form.get('nome_proprietario', '').strip()

        # Validações
        if not cidade:
            flash("A cidade é obrigatória.")
            return redirect('/add_imovel')
        if not rua:
            flash("A rua é obrigatória.")
            return redirect('/add_imovel')
        if not numero or not numero.isdigit():
            flash("O número do imóvel deve ser preenchido e conter apenas dígitos.")
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
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO imovel (rua, cidade, numero, complemento, cep, valor_aluguel, nome_proprietario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (rua, cidade, numero, complemento, cep, valor_aluguel, nome_proprietario))
            db.commit()
            flash("Imóvel adicionado com sucesso!")
        except Exception as e:
            db.rollback()
            flash(f"Ocorreu um erro ao adicionar o imóvel: {e}")
            return redirect('/add_imovel')

        return redirect('/')

    # Renderiza a página de formulário
    return render_template('imovel.html')


@app.route('/add_inquilino', methods=["GET", "POST"])
def add_inquilino():
    nome = cpf = telefone = data_nascimento = imovel_id = None  

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
            flash("O CPF não existe.")
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
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO inquilino (nome, cpf, telefone, data_nascimento, imovel_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (nome, cpf, telefone, data_nascimento, imovel_id))
            db.commit()

            if cursor.rowcount > 0:
                flash("Inquilino adicionado com sucesso!")
            else:
                flash("Erro ao adicionar o inquilino. Tente novamente.")
            cursor.close()

        except mysql.connector.Error as err:
            flash(f"Erro no banco de dados: {err}")
            print(f"Erro ao adicionar inquilino: {err}")
            return redirect('/add_inquilino')

        return redirect('/')

    # Para uma requisição GET, carrega os imóveis
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            id, 
            CONCAT(rua, ', ', numero, IF(complemento != '', CONCAT(', ', complemento), ''), ', ', cidade, ', CEP: ', cep) AS endereco
        FROM imovel
    """)
    imoveis = cursor.fetchall()

    # Passa as variáveis para o template, mesmo em uma requisição GET
    return render_template('inquilino.html', imoveis=imoveis, nome=nome, cpf=cpf, telefone=telefone, data_nascimento=data_nascimento, imovel_id=imovel_id)


@app.route('/excluir_inquilino/<int:id>', methods=['GET'])
def excluir_inquilino(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM inquilino WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        flash("Inquilino excluído com sucesso!", "success")
    except Exception as e:
        flash("Erro ao excluir inquilino: " + str(e), "danger")
    return redirect('/listar')

@app.route('/editar_inquilino/<int:id>', methods=['GET', 'POST'])
def editar_inquilino(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento']
        imovel_id = request.form['imovel_id']

        cursor.execute("""
            UPDATE inquilino SET nome = %s, cpf = %s, telefone = %s, data_nascimento = %s, imovel_id = %s
            WHERE id = %s
        """, (nome, cpf, telefone, data_nascimento, imovel_id, id))
        db.commit()
        cursor.close()
        flash("Inquilino editado com sucesso!", "success")
        return redirect('/listar')

    cursor.execute("SELECT * FROM inquilino WHERE id = %s", (id,))
    inquilino = cursor.fetchone()
    cursor.execute("SELECT id, rua, cidade FROM imovel")  # Para preencher o dropdown com imóveis
    imoveis = cursor.fetchall()
    cursor.close()
    return render_template('editar_inquilino.html', inquilino=inquilino, imoveis=imoveis)

# Rota para editar um imóvel
@app.route('/editar_imovel/<int:id>', methods=['GET', 'POST'])
def editar_imovel(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        rua = request.form['rua']
        cidade = request.form['cidade']
        numero = request.form['numero']
        complemento = request.form['complemento']
        cep = request.form['cep']
        valor_aluguel = request.form['valor_aluguel']
        nome_proprietario = request.form['nome_proprietario']

        cursor.execute("""
            UPDATE imovel SET rua = %s, cidade = %s, numero = %s, complemento = %s, cep = %s, valor_aluguel = %s, nome_proprietario = %s
            WHERE id = %s
        """, (rua, cidade, numero, complemento, cep, valor_aluguel, nome_proprietario, id))
        db.commit()
        cursor.close()
        flash("Imóvel editado com sucesso!", "success")
        return redirect('/listar')

    cursor.execute("SELECT * FROM imovel WHERE id = %s", (id,))
    imovel = cursor.fetchone()
    cursor.close()
    return render_template('editar_imovel.html', imovel=imovel)

# Rota para excluir um imóvel
@app.route('/excluir_imovel/<int:id>', methods=['GET'])
def excluir_imovel(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM inquilino WHERE imovel_id = %s", (id,))
    inquilinos = cursor.fetchall()

    if inquilinos:
        flash("Erro: Não é possível excluir o imóvel, pois existem inquilinos cadastrados nele.", "danger")
    else:
        cursor.execute("DELETE FROM imovel WHERE id = %s", (id,))
        db.commit()
        flash("Imóvel excluído com sucesso!", "success")
    cursor.close()
    return redirect('/listar')


# Rota para listar inquilinos e imóveis
@app.route('/listar')
def listar_inquilinos_imoveis():
    cursor = db.cursor(dictionary=True)

    # Consulta os dados dos inquilinos
    cursor.execute("SELECT id, nome, cpf, telefone, data_nascimento, imovel_id FROM inquilino")
    inquilinos = cursor.fetchall()

    # Consulta os dados dos imóveis
    cursor.execute("SELECT id, rua, cidade, numero, complemento, cep, valor_aluguel, nome_proprietario FROM imovel")
    imoveis = cursor.fetchall()

    cursor.close()

    return render_template('listar.html', inquilinos=inquilinos, imoveis=imoveis)



if __name__ == '__main__':
    app.run(debug=True)
