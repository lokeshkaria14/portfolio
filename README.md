# Portfolio Contact Form Setup

This setup uses Flask backend + Gmail SMTP to send contact form emails completely free.

## Prerequisites
- Python 3.7+
- Gmail account

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to **App passwords** 
4. Select "Mail" and "Windows Computer" (or your device)
5. Google will generate a 16-character password
6. Copy this password

### 3. Configure `.env` File

Edit `.env` and replace with your credentials:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_character_app_password_here
RECIPIENT_EMAIL=lokesh@lokeshkaria.dev
```

### 4. Run the Flask Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### 5. Test It!

- Keep the Flask server running
- Open `portfolio.html` in your browser
- Fill out the contact form and click "Send Message"
- Check your email inbox for the message!

## Important Notes

⚠️ **The Flask server must be running for the form to work!**

- For local testing: Run `python app.py` in a terminal
- The form will show an error if the server isn't running
- The form makes requests to `http://localhost:5000/send-email`

## Production Deployment

For live deployment (not local):
1. Set environment variables on your hosting platform (Heroku, Railway, etc.)
2. Update the form to send to your production URL instead of `localhost:5000`
3. Use a proper WSGI server like Gunicorn

Example for production:
```javascript
// Change this line in portfolio.html:
const response = await fetch('https://your-domain.com/send-email', {
```

## Troubleshooting

**"Is the server running?" error**
- Make sure you ran `python app.py` in a terminal
- Check that it's running on `http://localhost:5000`

**"Email authentication failed"**
- Double-check your `SENDER_EMAIL` and `SENDER_PASSWORD` in `.env`
- Make sure you're using the 16-character **app password**, not your Gmail password
- Verify 2-Step Verification is enabled

**No email received**
- Check your spam/junk folder
- Verify `RECIPIENT_EMAIL` in `.env` is correct
- Check browser console for errors (F12)
