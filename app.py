from flask import Flask, render_template, request
app = Flask(__name__)

# Hard-coded username and password for testing
valid_username = 'user'
valid_password = 'password'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == valid_username and password == valid_password:
            # Redirect to admin dashboard 
            return render_template('admin.html')
        else:
            # Render the login page again with an error message
            error_message = "Incorrect username or password. Please try again."
            return render_template('login.html', error=error_message)
    else:
        # GET request, render the login form
        return render_template('login.html')
    




if __name__ == '__main__':
    app.run(debug=True)
