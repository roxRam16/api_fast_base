from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de usuarios registrados
users = {"admin": "1234"}

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return f"Bienvenido, {username}!"
    return "Credenciales incorrectas", 401

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/create_account', methods=['POST'])
def create_account():
    username = request.form['username']
    password = request.form['password']
    users[username] = password
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
