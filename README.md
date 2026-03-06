# WhatsApp Message Sender with Flask & Twilio

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Twilio Credentials
1. Sign up at https://www.twilio.com/
2. Get your Account SID and Auth Token from the dashboard
3. Activate the WhatsApp Sandbox: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
4. Follow instructions to connect your WhatsApp number to the sandbox

### 3. Configure app.py
Replace these values in `app.py`:
- `TWILIO_ACCOUNT_SID` - Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` - Your Twilio Auth Token
- `TWILIO_WHATSAPP_NUMBER` - Your Twilio WhatsApp number (default sandbox: whatsapp:+14155238886)

### 4. Run the Application
```bash
python app.py
```

### 5. Access the App
Open your browser and go to: http://localhost:5000

### Usage
1. Enter the recipient's phone number (with country code, e.g., +1234567890)
2. Type your custom message
3. Click "Send WhatsApp Message"

**Note:** Recipients must join your Twilio sandbox first by sending a specific code to the Twilio WhatsApp number.
