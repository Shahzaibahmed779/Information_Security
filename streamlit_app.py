import streamlit as st
import requests

# Flask backend URL
BACKEND_URL = "http://127.0.0.1:5000"

st.title("Digital Rights Management System")

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['is_admin'] = False

# Login form
if not st.session_state['logged_in']:
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True
            st.session_state['is_admin'] = response.json()['is_admin']
        else:
            st.error("Invalid credentials!")

# Admin Dashboard
if st.session_state['logged_in'] and st.session_state['is_admin']:
    st.subheader("Admin Dashboard")

    # File upload for new content
    uploaded_file = st.file_uploader("Upload a New File", type=["png"])
    if uploaded_file and st.button("Upload File"):
        response = requests.post(f"{BACKEND_URL}/upload", files={"file": uploaded_file})
        if response.status_code == 200:
            st.success(response.json()['message'])
        else:
            st.error(response.json()['message'])

    # File tracing for watermark extraction
    trace_file = st.file_uploader("Upload a File to Trace", type=["png"])
    if trace_file and st.button("Trace File"):
        response = requests.post(f"{BACKEND_URL}/trace", files={"file": trace_file})
        if response.status_code == 200:
            st.write("Extracted Watermark:")
            st.write(response.json()['watermark'])
        else:
            st.error(response.json()['message'])

# Logout button
if st.session_state['logged_in']:
    if st.button("Logout"):
        requests.post(f"{BACKEND_URL}/logout")
        st.session_state['logged_in'] = False
        st.session_state['is_admin'] = False
        st.success("Logged out successfully!")
