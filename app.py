from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3
import os
from watermarker import embed_watermark, extract_watermark
import streamlit as st

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


@app.route('/')
def index():
    init_db()  # Initialize the database when the app starts
    return render_template('index.html')


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
            session['is_admin'] = email == "shahzaibahmed779@gmail.com"
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))

    if session.get('is_admin'):
        # Streamlit for admin features
        st.title("Admin Dashboard")
        st.write("Welcome, Admin!")

        # Upload a new file
        if st.button("Upload a New File"):
            uploaded_file = st.file_uploader("Choose a PNG file", type=["png"])
            if uploaded_file:
                file_path = os.path.join('static/images', uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Trace a file
        if st.button("Trace a File"):
            trace_file = st.file_uploader("Choose a watermarked PNG file to trace", type=["png"])
            if trace_file:
                trace_path = os.path.join('static/images', trace_file.name)
                with open(trace_path, "wb") as f:
                    f.write(trace_file.getbuffer())
                watermark = extract_watermark(trace_path)
                st.write("User's Credentials:")
                st.write(watermark)

        return st._main_run()

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
    print("Flask is running under Streamlit!")
