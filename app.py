from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Configuração de conexão com o banco (ajuste com seus dados)
DB_HOST = "localhost"
DB_NAME = ""
DB_USER = ""
DB_PASS = ""


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM produto ORDER BY id;')
    produtos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', produtos=produtos)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO produto (nome, quantidade, preco) VALUES (%s, %s, %s)',
                (nome, quantidade, preco))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)