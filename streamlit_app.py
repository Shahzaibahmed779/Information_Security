import streamlit as st
import sqlite3
import os
from watermarker import embed_watermark, extract_watermark
from PIL import Image

# Database Initialization
DATABASE = "users.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, phone, password) 
        VALUES ("shahzaibahmed779@gmail.com", "03145276032", "f1h24*659/")
    ''')  # Hardcoded admin credentials
    conn.commit()
    conn.close()

# User Authentication
def authenticate_user(email, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Streamlit App
st.title("Digital Rights Management System")
init_db()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["is_admin"] = False

if not st.session_state["logged_in"]:
    # Login Form
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = user[1]
            st.session_state["is_admin"] = (user[1] == "shahzaibahmed779@gmail.com")
            st.success(f"Welcome, {st.session_state['user_email']}!")
        else:
            st.error("Invalid email or password.")

else:
    # Dashboard for Logged-In Users
    st.subheader("Dashboard")
    st.write(f"Logged in as: {st.session_state['user_email']}")

    if st.session_state["is_admin"]:
        st.info("Admin Privileges Enabled")

        # Admin: Upload a New File
        st.subheader("Upload a New PNG File")
        new_file = st.file_uploader("Upload a PNG file", type=["png"])
        if new_file:
            file_path = os.path.join("uploads", new_file.name)
            with open(file_path, "wb") as f:
                f.write(new_file.getbuffer())
            st.success(f"File '{new_file.name}' uploaded successfully!")

        # Admin: Trace Watermark
        st.subheader("Trace a Watermarked File")
        trace_file = st.file_uploader("Upload a watermarked PNG file to trace", type=["png"])
        if trace_file:
            trace_path = os.path.join("uploads", trace_file.name)
            with open(trace_path, "wb") as f:
                f.write(trace_file.getbuffer())
            watermark = extract_watermark(trace_path)
            st.write("Extracted User's Credentials:")
            st.json(watermark)

    # Regular User: Download Watermarked Images
    st.subheader("Download Watermarked Image")
    download_file = st.selectbox(
        "Select a file to download",
        os.listdir("uploads") if os.path.exists("uploads") else []
    )
    if st.button("Download"):
        if download_file:
            file_path = os.path.join("uploads", download_file)
            watermarked_path = os.path.join("downloads", f"watermarked_{download_file}")
            embed_watermark(file_path, watermarked_path, f"{st.session_state['user_email']}|{st.session_state['user_email']}")
            st.download_button(
                label="Download Watermarked Image",
                data=open(watermarked_path, "rb").read(),
                file_name=f"watermarked_{download_file}"
            )
        else:
            st.error("No file selected.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["is_admin"] = False
        st.session_state["user_email"] = None
        st.success("Logged out successfully!")

