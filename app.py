from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import Flask, render_template
import smtplib
import os
import traceback

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Validate environment variables on startup
missing = []

if not SENDER_EMAIL:
    missing.append("SENDER_EMAIL")

if not APP_PASSWORD:
    missing.append("APP_PASSWORD")

if not RECIPIENT_EMAIL:
    missing.append("RECIPIENT_EMAIL")

if missing:
    raise ValueError(
        f"Missing environment variables: {', '.join(missing)}"
    )


@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid JSON payload"
            }), 400

        required_fields = [
            "fname",
            "lname",
            "email",
            "subject",
            "msg"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing field: {field}"
                }), 400

        fname = data["fname"].strip()
        lname = data["lname"].strip()
        email = data["email"].strip()
        subject = data["subject"].strip()
        message = data["msg"].strip()

        if not all([
            fname,
            lname,
            email,
            subject,
            message
        ]):
            return jsonify({
                "success": False,
                "error": "All fields are required"
            }), 400

        # Basic email validation
        if "@" not in email:
            return jsonify({
                "success": False,
                "error": "Invalid email address"
            }), 400

        body = f"""
New portfolio contact form submission

Name: {fname} {lname}
Email: {email}

Subject:
{subject}

Message:
{message}
"""

        msg = MIMEText(body)

        msg["Subject"] = f"Portfolio Contact: {subject}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL

        # Clicking reply in Gmail replies to the visitor
        msg["Reply-To"] = email

        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465,
            timeout=30
        ) as smtp:

            print("Connected.")

            smtp.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            print("Authenticated.")

            smtp.send_message(msg)

            print("Email sent.")

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except smtplib.SMTPAuthenticationError:
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": "SMTP authentication failed. Check Gmail App Password."
        }), 500

    except Exception:
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": "Failed to send email"
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "email_configured": bool(
            SENDER_EMAIL and
            APP_PASSWORD and
            RECIPIENT_EMAIL
        )
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )