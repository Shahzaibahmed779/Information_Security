from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3
import os
from watermarker import embed_watermark

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
    conn.commit()
    conn.close()


@app.route('/')
def index():
    init_db()  # Initialize the database when the app starts
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']  # Storing plaintext password

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (email, phone, password) VALUES (?, ?, ?)', (email, phone, password))
            conn.commit()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            if "email" in str(e):  # Check if the error is due to the email
                flash('Email is already registered. Please use a different email.', 'danger')
            elif "phone" in str(e):  # Check if the error is due to the phone number
                flash('Phone number is already registered. Please use a different phone number.', 'danger')
            else:
                flash('An unexpected error occurred. Please try again.', 'danger')
            return redirect(url_for('register'))

        finally:
            # Ensure the database connection is always closed
            conn.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        if user and password == user['password']:
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['phone'] = user['phone']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/download', methods=['POST'])
def download():
    if 'user_id' not in session:
        flash('Please log in to download images.', 'warning')
        return redirect(url_for('login'))

    # Path to save records
    base_record_path = r'C:\Users\Mahnoor\Desktop\University\IS\Term-Project\Record'

    # Extract email from the session
    user_email = session['email']

    # Create a folder named after the email
    user_folder = os.path.join(base_record_path, user_email)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Requested image
    image_name = request.form['image']
    original_image_path = os.path.join('static', 'images', image_name)

    # Save watermarked image in the user's folder
    watermarked_image_path = os.path.join(user_folder, f"watermarked_{image_name}")

    # Watermark text
    watermark_text = f"{user_email}|{session['phone']}"
    embed_watermark(original_image_path, watermarked_image_path, watermark_text)

    # Return the file to the user without saving it in the project directory
    return send_file(watermarked_image_path, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
