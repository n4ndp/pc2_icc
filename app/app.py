from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)
app.secret_key = 'mys3cr3tk3y'

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'rootpassword')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'flaskapp')

mysql = MySQL(app)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['nombre'] = account['nombre']
            flash(f"Bienvenido, {account['nombre']}!")
            return redirect('/users')
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash('El username ya existe, elige otro')
        else:
            cursor.execute('INSERT INTO users (nombre, username, password) VALUES (%s, %s, %s)', (nombre, username, password))
            mysql.connection.commit()
            flash('Registro exitoso. Ahora inicia sesión.')
            return redirect('/login')
    return render_template('register.html')

@app.route('/users')
def users():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id, nombre, username FROM users')
        users = cursor.fetchall()
        return render_template('users.html', users=users, nombre=session.get('nombre'))
    return redirect('/login')

@app.route('/delete/<int:id>')
def delete_user(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Usuario eliminado')
        return redirect('/users')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
