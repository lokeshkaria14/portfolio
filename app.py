from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask import render_template
import os
import traceback
import resend

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

resend.api_key = RESEND_API_KEY
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Validate environment variables on startup
missing = []

if not RESEND_API_KEY:
    missing.append("RESEND_API_KEY")

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

        params = {
            "from": "onboarding@resend.dev",
            "to": [RECIPIENT_EMAIL],
            "subject": f"Portfolio Contact: {subject}",
            "html": f"""
            <h2>New Portfolio Contact Form Submission</h2>

            <p><strong>Name:</strong> {fname} {lname}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>

            <hr>

            <p>{message}</p>
            """
        }

        response = resend.Emails.send(params)

        print("RESEND RESPONSE:")
        print(response)

        return jsonify({
            "success": True,
            "message": "Email sent successfully"
        })

    except Exception as e:
        print("ERROR:")
        print(e)
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "email_configured": bool(
            RESEND_API_KEY and
            RECIPIENT_EMAIL
        )
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )