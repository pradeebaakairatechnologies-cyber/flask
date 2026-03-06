from flask import Flask, render_template, request, jsonify
import os
import requests
from werkzeug.utils import secure_filename
import base64
from flask_mail import Mail, Message
import traceback

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@womensday.com')
app.config['MAIL_SUPPRESS_SEND'] = not (app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD'])

mail = Mail(app)

# Google Apps Script URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbytB-Z0w0-LikTqGOYFIM-oKkdAMtEHxMGc1YK1tCxGo9AxwPSym9yb1Z4o2GXn921d/exec"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    try:
        print('Starting registration submission...')
        
        # Get form data
        participant_email = request.form.get('email', '').strip()
        participant_name = request.form.get('participantName', '').strip()
        age = request.form.get('age', '').strip()
        phone_number = request.form.get('phoneNumber', '').strip()
        address = request.form.get('address', '').strip()
        group1 = request.form.get('group1', '').strip()
        group2 = request.form.get('group2', '').strip()
        group3 = request.form.get('group3', '').strip()
        
        print(f'Form data received: {participant_name}, {participant_email}')
        
        # Validate required fields
        if not all([participant_email, participant_name, age, phone_number, address]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get file
        file = request.files.get('paymentScreenshot')
        if not file or file.filename == '':
            return jsonify({'success': False, 'error': 'Payment screenshot required'}), 400
        
        print(f'File received: {file.filename}, size: {len(file.read())} bytes')
        file.seek(0)  # Reset file pointer
        
        # Read file and convert to base64
        file_content = file.read()
        base64_file = base64.b64encode(file_content).decode('utf-8')
        
        print('Converting to base64...')
        
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
        
        print('Sending to Google Sheets...')
        # Send to Google Sheets
        response = requests.post(GOOGLE_SCRIPT_URL, data=form_data, timeout=30)
        print(f'Google Sheets response: {response.status_code}')
        
        if response.status_code != 200:
            return jsonify({'success': False, 'error': 'Failed to submit to Google Sheets'}), 400
        
        # Send email confirmation
        try:
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                msg = Message(
                    subject='Women\'s Day Event Registration Confirmation',
                    recipients=[participant_email],
                    html=f"""
                    <h2>Registration Confirmed!</h2>
                    <p>Hi {participant_name},</p>
                    <p>Thank you for registering for Women's Day Event!</p>
                    <p><strong>Registration Details:</strong></p>
                    <ul>
                        <li>Name: {participant_name}</li>
                        <li>Age: {age}</li>
                        <li>Phone: +91{phone_number}</li>
                        <li>Address: {address}</li>
                        <li>Group 1: {group1 or 'Not selected'}</li>
                        <li>Group 2: {group2 or 'Not selected'}</li>
                        <li>Group 3: {group3 or 'Not selected'}</li>
                    </ul>
                    <p>We're excited to have you participate. See you soon!</p>
                    """
                )
                mail.send(msg)
                print('Email sent successfully')
            else:
                print('Email credentials not configured')
        except Exception as email_error:
            print(f'Email error (non-blocking): {str(email_error)}')
        
        return jsonify({'success': True, 'message': 'Registration submitted successfully'})
    
    except Exception as e:
        print(f'Registration error: {str(e)}')
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

