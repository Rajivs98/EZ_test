from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import psycopg2
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)

# Configure your PostgreSQL database connection
db_connection = psycopg2.connect(
    host="your_db_host",
    user="your_db_user",
    password="your_db_password",
    database="your_db_name"
)

# Define a function to check if a user is an Ops User
def is_ops_user(username):
    # Implement your logic to check if the user is an Ops User
    # You can fetch this information from the database
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT is_ops_user FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
    return False

# Define a function to generate a secure link for downloading
def generate_secure_link(username, filename):
    # Generate a secure token for the link (You can use a better method for security)
    token = secrets.token_hex(16)
    # Store the token and associate it with the user and file
    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO secure_links (token, username, filename) VALUES (%s, %s, %s)", (token, username, filename))
    return token

# ... (Rest of the Flask app remains the same)
# User Registration (for Client Users)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']

    # Store user data securely (e.g., in a database)
    with db_connection.cursor() as cursor:
        cursor.execute("INSERT INTO users (username, password, email, is_ops_user) VALUES (%s, %s, %s, %s)", (username, password, email, False))

    # Send a verification email to the user's registered email address
    send_verification_email(email, username)

    # Generate an encrypted URL (You can use a library like Flask-Security for this)
    encrypted_url = generate_secure_link(username, 'verification.pdf')  # Replace with actual encryption logic
    return jsonify({'encrypted_url': encrypted_url})

# Email Verification (for Client Users)
def send_verification_email(email, username):
    # Implement your email sending logic here using SMTP or an email service provider
    # You can use the 'smtplib' library to send emails
    # Include a link to verify the email
    pass

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if the user exists and the password is correct
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and result[1] == password:
            return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'})



# Upload File (for Ops Users)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and file.filename.lower().endswith(('.pptx', '.docx', '.xlsx')) and is_ops_user(username):
        # Save the uploaded file (You can use a storage system like Amazon S3)
        # Implement your file-saving logic here, for example:
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        # Store information about the uploaded file
        with db_connection.cursor() as cursor:
            cursor.execute("INSERT INTO uploaded_files (filename, username, file_path) VALUES (%s, %s, %s)", (filename, username, file_path))

        return jsonify({'message': 'File uploaded successfully'})
    else:
        return jsonify({'message': 'File upload failed'})



# Download File (for Client Users)
@app.route('/download/<token>', methods=['GET'])
def download_file(token):
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT username, filename FROM secure_links WHERE token = %s", (token,))
        link_info = cursor.fetchone()

    if link_info:
        link_username, filename = link_info
        # Check if the user has permission to download the file
        if not is_ops_user(link_username):
            return jsonify({'message': 'Permission denied'})

        # Provide a secure way to download the file (e.g., using Flask's send_file)
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT file_path FROM uploaded_files WHERE filename = %s", (filename,))
            file_path = cursor.fetchone()

        if file_path:
            file_path = file_path[0]
            return send_file(file_path, as_attachment=True)

    return jsonify({'message': 'Invalid or expired download link'})


# List all uploaded files (for Client Users)
@app.route('/list-files', methods=['GET'])
def list_files():
    if not is_ops_user(username):
        return jsonify({'message': 'Permission denied'})

    # Provide a list of all uploaded files (you can filter this based on user if needed)
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT filename FROM uploaded_files")
        files = cursor.fetchall()

    return jsonify([file[0] for file in files])
