from flask import Flask, request, jsonify
import sqlite3
import bcrypt

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password_hash TEXT)''')
conn.commit()

def register_user(username, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        password_hash = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)
    return False

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    if register_user(username, password):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'User already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if validate_user(username, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(port=5800)
