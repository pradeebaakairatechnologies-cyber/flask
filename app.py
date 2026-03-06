from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'your_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_auth_token_here'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio sandbox number

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        data = request.json
        to_number = data.get('to_number')
        message = data.get('message')
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        
        return jsonify({'success': True, 'message_sid': message.sid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
