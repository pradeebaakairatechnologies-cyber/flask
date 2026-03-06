from flask import Flask, render_template, request, jsonify
import os
import requests
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__, static_folder='static', static_url_path='/static')

# WhatsApp server URL
WHATSAPP_SERVER_URL = os.getenv('WHATSAPP_SERVER_URL', 'http://localhost:3001')

# Google Apps Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbytB-Z0w0-LikTqGOYFIM-oKkdAMtEHxMGc1YK1tCxGo9AxwPSym9yb1Z4o2GXn921d/exec"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    try:
        # Get form data
        participant_name = request.form.get('participantName')
        age = request.form.get('age')
        phone_number = request.form.get('phoneNumber')
        address = request.form.get('address')
        group1 = request.form.get('group1', '')
        group2 = request.form.get('group2', '')
        group3 = request.form.get('group3', '')
        
        # Get file
        file = request.files.get('paymentScreenshot')
        
        if not file:
            return jsonify({'success': False, 'error': 'Payment screenshot required'}), 400
        
        # Read file and convert to base64
        file_content = file.read()
        base64_file = base64.b64encode(file_content).decode('utf-8')
        
        # Prepare data for Google Sheets
        form_data = {
            'participantName': participant_name,
            'age': age,
            'phoneNumber': f'+91{phone_number}',
            'address': address,
            'group1': group1,
            'group2': group2,
            'group3': group3,
            'base64File': base64_file,
            'fileName': secure_filename(file.filename),
            'mimeType': file.mimetype
        }
        
        # Send to Google Sheets
        response = requests.post(GOOGLE_SCRIPT_URL, data=form_data, timeout=30)
        
        if response.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to submit to Google Sheets'}), 400
        
        # Send WhatsApp confirmation
        try:
            whatsapp_response = requests.post(
                f'{WHATSAPP_SERVER_URL}/send-message',
                json={
                    'phoneNumber': f'+91{phone_number}',
                    'message': f"Hi {participant_name}, Thank you for registering for Women's Day Event! We're excited to have you participate. See you soon!"
                },
                timeout=10
            )
            print(f'WhatsApp response: {whatsapp_response.status_code}')
        except Exception as whatsapp_error:
            print(f'WhatsApp error (non-blocking): {str(whatsapp_error)}')
        
        return jsonify({'success': True, 'message': 'Registration submitted successfully'})
    
    except Exception as e:
        print(f'Registration error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 400

