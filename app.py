from flask import Flask, jsonify, request, session
import sqlite3
import os
from watermarker import embed_watermark, extract_watermark

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'users.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insert hardcoded admin credentials if not already in the database
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, phone, password) 
        VALUES ("shahzaibahmed779@gmail.com", "03145276032", "f1h24*659/")
    ''')
    conn.commit()
    conn.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user and password == user['password']:
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['phone'] = user['phone']
        session['is_admin'] = email == "shahzaibahmed779@gmail.com"
        return jsonify({'status': 'success', 'is_admin': session['is_admin']}), 200
    else:
        return jsonify({'status': 'failed', 'message': 'Invalid email or password'}), 401


@app.route('/upload', methods=['POST'])
def upload():
    if 'is_admin' not in session or not session['is_admin']:
        return jsonify({'status': 'failed', 'message': 'Unauthorized'}), 403

    uploaded_file = request.files.get('file')
    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({'status': 'failed', 'message': 'No file provided'}), 400

    file_path = os.path.join('static/images', uploaded_file.filename)
    uploaded_file.save(file_path)
    return jsonify({'status': 'success', 'message': f'File {uploaded_file.filename} uploaded successfully!'}), 200


@app.route('/trace', methods=['POST'])
def trace():
    if 'is_admin' not in session or not session['is_admin']:
        return jsonify({'status': 'failed', 'message': 'Unauthorized'}), 403

    uploaded_file = request.files.get('file')
    if not uploaded_file or uploaded_file.filename == '':
        return jsonify({'status': 'failed', 'message': 'No file provided'}), 400

    file_path = os.path.join('static/images', uploaded_file.filename)
    uploaded_file.save(file_path)
    watermark = extract_watermark(file_path)
    return jsonify({'status': 'success', 'watermark': watermark}), 200


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out successfully'}), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
