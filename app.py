from flask import Flask, request, jsonify
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.auth import default
import google.auth
from email.mime.text import MIMEText
import base64
import os
from dotenv import load_dotenv
import httplib2
from googleapiclient.discovery import build

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "lokesh@lokeshkaria.dev")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

def get_gmail_service():
    """Authenticate with Google and return Gmail service."""
    try:
        credentials = Credentials.from_service_account_file(
            GOOGLE_APPLICATION_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )
        service = build('gmail', 'v1', credentials=credentials)
        return service
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise

def send_gmail(service, sender, to, subject, message_text):
    """Send email using Gmail API."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    try:
        message_obj = {'raw': raw_message}
        service.users().messages().send(userId='me', body=message_obj).execute()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        
        # Validate input
        required_fields = ['fname', 'lname', 'email', 'subject', 'msg']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        fname = data['fname'].strip()
        lname = data['lname'].strip()
        email = data['email'].strip()
        subject = data['subject'].strip()
        msg_body = data['msg'].strip()
        
        if not all([fname, lname, email, subject, msg_body]):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        # Build email message
        message_body = f"""
New contact form submission:

Name: {fname} {lname}
Email: {email}
Subject: {subject}

Message:
{msg_body}
        """
        
        # Get Gmail service and send email
        service = get_gmail_service()
        send_gmail(
            service,
            SENDER_EMAIL,
            RECIPIENT_EMAIL,
            f"Portfolio Contact: {subject}",
            message_body
        )
        
        return jsonify({'success': True, 'message': 'Email sent successfully!'})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to send email. Please try again.'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
