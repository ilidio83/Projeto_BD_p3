from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "Projeto_bd"
DB_USER = "postgres"
DB_PASS = "091020"


def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM vw_relatorio_estoque ORDER BY id;')
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
    cur.execute('INSERT INTO produto (nome, quantidade, preco) VALUES (%s, %s, %s)', (nome, quantidade, preco))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


@app.route('/dar_desconto', methods=['POST'])
def dar_desconto():
    percentual = request.form['percentual']

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('CALL sp_aplicar_desconto_geral(%s)', (percentual,))

    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)