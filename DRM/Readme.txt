
README: Digital Rights Management System

 Overview

This is a Digital Rights Management System built with Streamlit and Python. The app allows users to register, log in, watermark images with embedded user credentials, and extract watermarks. It currently supports only PNG files.



Prerequisites
1. Python: Ensure you have Python 3.10 or higher installed.
2. Dependencies: Install required Python packages using `pip`.



Installation
1. Install required Python libraries:
    bash pip install -r requirements.txt
   

2. Ensure the `uploads` and `downloads` directories exist:
    bash mkdir uploads downloads 



 Running the App
1. Start the Streamlit app:
   Bash streamlit run streamlit_app.py
   

2. Open the provided URL in your browser (usually `http://localhost:8501`).



 Usage Instructions
1. Sign Up:
   - Enter your email, phone number, and password to register.
   - You will be redirected to the login page.

2. Log In:
   - Enter your registered email and password to access the dashboard.

3. Admin Features:
   - Upload images for watermarking or tracing watermarks.
   - Extract watermarks to verify user credentials.

4. User Features:
   - Download watermarked images directly after watermark embedding.



 Supported Image Formats
- PNG



Note
Ensure all image files are uploaded in supported formats. The app will convert images to RGB internally for watermarking.

Additionally, admin credentials are hardcoded for demonstration purposes:
Email: shahzaibahmed779@gmail.com
Phone: 03145276032
Password: f1h24*659/

