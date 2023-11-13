from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joaomysql'
app.config['MYSQL_DB'] = 'cadastroatletas'

mysql = MySQL(app)

# Criação da tabela
with app.app_context():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS atletas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Genero VARCHAR(255),
            categoria VARCHAR(255),
            nome VARCHAR(255),
            email VARCHAR(255),
            senha VARCHAR(255)
        )
    ''')
    mysql.connection.commit()
    cur.close()

@app.route('/')
def index():
    return render_template('cadastro.html')

@app.route('/loginatletas', methods=['POST'])
def cadastrar_atleta():
    try:
        if request.method == 'POST':
            detalhes_atleta = request.form
            genero = detalhes_atleta['genero']
            categoria = detalhes_atleta['categoria']
            nome = detalhes_atleta['nome']
            email_atleta = detalhes_atleta['email']
            senha = detalhes_atleta['senha']

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO atletas(Genero, categoria, nome, email, senha) VALUES (%s, %s, %s, %s, %s)",
                (genero, categoria, nome, email_atleta, senha)
            )
            mysql.connection.commit()
            cur.close()

            return 'Cadastro realizado com sucesso!'
    except Exception as e:
        print("Erro interno do servidor:", str(e))
        return 'Erro interno do servidor', 500

if __name__ == '__main__':
    app.run(debug=True)
