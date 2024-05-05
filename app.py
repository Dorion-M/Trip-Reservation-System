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
    cur = db.execute("SELECT seatRow, seatColumn FROM reservations")
    reserved_seats = cur.fetchall()
    seat_matrix = [['O' for _ in range(4)] for _ in range(12)]  #Create a 12x4 matrix of 'O'

    #Update the matrix with 'X' where seats are reserved
    for row, col in reserved_seats:
        seat_matrix[row][col] = 'X'
    
    total_sales = sum(get_cost_matrix()[row][col] if seat == 'X' else 0 
                      for row, line in enumerate(seat_matrix) 
                      for col, seat in enumerate(line))

    return render_template('admin.html', seat_matrix=seat_matrix, total_sales=total_sales)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
