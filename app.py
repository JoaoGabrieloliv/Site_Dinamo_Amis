from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Adiciona o CORS ao seu app Flask

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joaomysql'
app.config['MYSQL_DB'] = 'cadastroatletas'

mysql = MySQL(app)

def criar_tabela():
    try:
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
    except Exception as e:
        print("Erro ao criar tabela:", str(e))

criar_tabela()

@app.route('/cadastro', methods=['POST'])
def cadastrar_atleta():
    try:
        if request.method == 'POST':
            detalhes_atleta = request.form
            genero = detalhes_atleta['genero']
            categoria = detalhes_atleta['categoria']
            nome = detalhes_atleta['nome']
            email_atleta = detalhes_atleta['email']
            senha = detalhes_atleta['senha']

            if genero and categoria and nome and email_atleta and senha:
                cur = mysql.connection.cursor()
                cur.execute("SELECT id FROM atletas WHERE email = %s", (email_atleta,))
                usuario_existente = cur.fetchone()

                if usuario_existente:
                    cur.close()
                    return jsonify({'status': 'UsuarioExistente'})
                else:
                    cur.execute(
                        "INSERT INTO atletas(Genero, categoria, nome, email, senha) VALUES (%s, %s, %s, %s, %s)",
                        (genero, categoria, nome, email_atleta, senha)
                    )
                    mysql.connection.commit()
                    cur.close()
                    return jsonify({'status': 'CadastroSucesso'})
            else:
                return jsonify({'status': 'CamposVazios'}), 400
    except Exception as e:
        print("Erro interno do servidor:", str(e))
        return jsonify({'status': 'ErroServidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
