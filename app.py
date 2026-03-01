from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar Banco de Dados
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            descricao TEXT,
            entrada REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            descricao TEXT,
            saida REAL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receitas")
    receitas = cursor.fetchall()

    cursor.execute("SELECT * FROM gastos")
    gastos = cursor.fetchall()

    total_receita = sum([r[3] for r in receitas])
    total_gasto = sum([g[3] for g in gastos])
    saldo = total_receita - total_gasto

    conn.close()

    return render_template(
        'index.html',
        receitas=receitas,
        gastos=gastos,
        total_receita=total_receita,
        total_gasto=total_gasto,
        saldo=saldo
    )

@app.route('/add_receita', methods=['POST'])
def add_receita():
    data = request.form['data']
    descricao = request.form['descricao']
    entrada = float(request.form['entrada'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO receitas (data, descricao, entrada) VALUES (?, ?, ?)",
                   (data, descricao, entrada))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/add_gasto', methods=['POST'])
def add_gasto():
    data = request.form['data']
    descricao = request.form['descricao']
    saida = float(request.form['saida'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gastos (data, descricao, saida) VALUES (?, ?, ?)",
                   (data, descricao, saida))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete_receita/<int:id>')
def delete_receita(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM receitas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/delete_gasto/<int:id>')
def delete_gasto(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gastos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)