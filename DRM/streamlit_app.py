import streamlit as st
import sqlite3
import os
from watermark_utils import embed_watermark, extract_watermark
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

def register_user(email, phone, password):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, phone, password) VALUES (?, ?, ?)", (email, phone, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Ensure directories exist
def ensure_directories():
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

# Initialize the app
init_db()
ensure_directories()

# Streamlit App
st.title("Digital Rights Management System")

# Session Variables Initialization
if "page" not in st.session_state:
    st.session_state["page"] = "signup"  # Default to signup page
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    st.session_state["is_admin"] = False

# Page Navigation Logic
def navigate_to(page_name):
    st.session_state["page"] = page_name

# Signup Page
if st.session_state["page"] == "signup" and not st.session_state["logged_in"]:
    st.subheader("Signup")
    email = st.text_input("Email", key="signup_email")
    phone = st.text_input("Phone Number", key="signup_phone")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Signup"):
        if not email or not phone or not password:
            st.error("All fields are required.")
        elif register_user(email, phone, password):
            st.session_state["phone"] = phone  # Add this line to take phone number to the next page
            st.success("Signup successful! Redirecting to login...")
            navigate_to("login")
        else:
            st.error("Email or phone number already registered. Try again.")
    if st.button("Go to Login"):
        navigate_to("login")

# Login Page
if st.session_state["page"] == "login" and not st.session_state["logged_in"]:
    st.subheader("Login")
    email = st.text_input("Login Email", key="login_email")
    password = st.text_input("Login Password", type="password", key="login_password")
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = user[1]  # Email
            st.session_state["phone"] = user[2]  # Phone number
            st.session_state["is_admin"] = (user[1] == "shahzaibahmed779@gmail.com")
            navigate_to("dashboard")
        else:
            st.error("Invalid email or password.")

# Dashboard Page
if st.session_state["page"] == "dashboard" and st.session_state["logged_in"]:
    st.subheader("Dashboard")
    st.write(f"Logged in as: {st.session_state['user_email']}")

    if st.session_state["is_admin"]:
        st.info("Admin Privileges Enabled")
        # Admin: Upload a New File
        new_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "bmp", "tiff"])
        if new_file:
            file_path = os.path.join("uploads", new_file.name)
            with open(file_path, "wb") as f:
                f.write(new_file.getbuffer())
            st.success(f"File '{new_file.name}' uploaded successfully!")

        # Admin: Trace Watermark
        trace_file = st.file_uploader("Upload a watermarked file to trace", type=["png", "jpg", "jpeg", "bmp", "tiff"])
        if trace_file:
            trace_path = os.path.join("uploads", trace_file.name)
            with open(trace_path, "wb") as f:
                f.write(trace_file.getbuffer())
            try:
                watermark = extract_watermark(trace_path)
                st.write("Extracted User's Credentials:")
                st.text(watermark)  # Show as plain text
            except Exception as e:
                st.error(f"Error extracting watermark: {str(e)}")

    # Regular User: Download Watermarked Images
    download_file = st.selectbox(
        "Select a file to download",
        os.listdir("uploads") if os.path.exists("uploads") else []
    )
    if st.button("Download"):
        if download_file:
            file_path = os.path.join("uploads", download_file)
            embed_watermark(
                file_path,
                file_path,  # Save with the same name
                f"{st.session_state['user_email']}|{st.session_state['phone']}"
            )
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Click here!",
                    data=f,
                    file_name=download_file
                )
        else:
            st.error("No file selected.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        navigate_to("signup")
