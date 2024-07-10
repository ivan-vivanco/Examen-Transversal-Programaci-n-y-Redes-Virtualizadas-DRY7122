import sqlite3
import hashlib

# Crear la base de datos
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Crear la tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT
    );
''')

# Función para almacenar usuarios y contraseñas en hash
def store_user(username, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()

# Función para validar usuarios
def validate_user(username, password):
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        stored_hash = row[0]
        calculated_hash = hashlib.sha256(password.encode()).hexdigest()
        return stored_hash == calculated_hash
    return False

# Ejemplo de uso de las funciones
store_user('Ivan', 'Vivanco1')
store_user('Sebastian', 'Toro2')

# Validar usuarios
print(validate_user('Ivan', 'Vivanco1'))  # True
print(validate_user('Sebastian', 'Toro2'))  # True
print(validate_user('user1', 'wrong_password'))  # False

# Cerrar la conexión a la base de datos
conn.close()
