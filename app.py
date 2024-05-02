from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

DATABASE = 'reservations.db'

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        cur = db.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        result = cur.fetchone()
        if result:
            return redirect(url_for('admin'))
        else:
            error_message = "Incorrect username or password. Please try again."
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')

@app.route('/admin')
def admin():
    db = get_db()
    cur = db.execute("SELECT * FROM reservations")
    reservations = cur.fetchall()
    total_sales = sum(get_cost_matrix()[row][col] for _, _, row, col, _, _ in reservations)
    return render_template('admin.html', reservations=reservations, total_sales=total_sales)

if __name__ == '__main__':
    app.run(debug=True)
