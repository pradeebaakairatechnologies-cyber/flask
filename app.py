from flask import Flask, render_template, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    try:
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            return jsonify({'success': False, 'error': 'Twilio credentials not configured'}), 500
        
        data = request.json
        to_number = data.get('to_number')
        message = data.get('message')
        
        if not to_number or not message:
            return jsonify({'success': False, 'error': 'Missing phone number or message'}), 400
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        msg = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        
        return jsonify({'success': True, 'message_sid': msg.sid})
    except Exception as e:
        print(f'Twilio Error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
