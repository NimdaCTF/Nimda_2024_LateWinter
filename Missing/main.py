from flask import Flask, render_template, request, session, redirect
import sqlite3
from hashlib import md5
from core import flag_config
import hmac
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)
admin = None


def generate_flag(user_id):
    PREFIX = flag_config['prefix']
    SECRET = flag_config['secret'].encode()
    SALT_SIZE = flag_config['salt_size']

    return PREFIX + hmac.new(SECRET, str(user_id).encode(), "sha256").hexdigest()[:SALT_SIZE]


@app.route('/', methods=['GET'])
def on_root_get():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def on_login():
    global admin

    connection = sqlite3.connect('db.sqlite3')
    if not request.form.get('login') or not request.form.get('password'):
        return 'Bad request', 400

    cursor = connection.cursor()
    password = None

    try:
        cursor.execute('SELECT password FROM Users where username = ?', (request.form['login'],))
        password = cursor.fetchone()[0]
    except:
        pass
    finally:
        cursor.close()

    if not password:
        return 'No', 401

    if md5(request.form['password'].encode()).hexdigest() != password:
        return 'No', 401

    if not admin:
        with open('admin', 'r', encoding='UTF-8') as f:
            admin = f.read()

    session['is_admin'] = admin == request.form['login']
    session['username'] = request.form['login']

    return redirect('/flag')


@app.route('/flag', methods=['GET'])
def on_flag():
    if not request.cookies.get('id'):
        return 'Rerun task or contact CTF admin. I don\'t have ur ID', 400

    if not session.get('username'):
        return 'No', 401

    if session.get('is_admin') is True:
        return render_template('flag.html', TEXT=generate_flag(request.cookies['id']), IS_ADMIN=True)

    return render_template('flag.html', TEXT=f'Hi, {session["username"]}. You\'re a regular user :D', IS_ADMIN=False)


@app.route('/logout', methods=['GET'])
def on_logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
