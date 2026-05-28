from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = ""
DB_USER = ""
DB_PASS = ""


def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)


# Listar tudo usando a View
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
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO produto (nome, quantidade, preco) VALUES (%s, %s, %s)', (nome, quantidade, preco))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


# DELETE Deletar via Procedure
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CALL sp_deletar_produto(%s)', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


## UPDATE
@app.route('/editar/<int:id>')
def editar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM produto WHERE id = %s', (id,))
    produto = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('editar.html', produto=produto)


## UPDATE - Parte 2 Salva a edição via Procedure
@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = int(request.form['id'])
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CALL sp_atualizar_produto(%s, %s, %s, %s)', (id, nome, quantidade, preco))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


# DESCONTO ESPECÍFICO Via Procedure
@app.route('/dar_desconto_item', methods=['POST'])
def dar_desconto_item():
    id = int(request.form['id'])
    percentual = float(request.form['percentual'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CALL sp_aplicar_desconto_produto(%s, %s)', (id, percentual))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


##DESCONTO GERAL Via Procedure
@app.route('/dar_desconto', methods=['POST'])
def dar_desconto():
    percentual = float(request.form['percentual'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CALL sp_aplicar_desconto_geral(%s)', (percentual,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)