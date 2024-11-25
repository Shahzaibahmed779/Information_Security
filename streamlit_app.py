import streamlit as st
import requests

# Flask backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# Streamlit interface
st.title("Digital Rights Management System")

# Login Form
with st.form("login_form"):
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

if login_button:
    response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        st.success("Logged in successfully!")
        st.session_state["user"] = response.json()  # Save user data in session state
    else:
        st.error("Invalid credentials!")

# Example button to test Flask route
if st.button("Get Dashboard Data"):
    response = requests.get(f"{BACKEND_URL}/dashboard")
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to fetch dashboard data.")
