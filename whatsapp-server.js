const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());
app.use(cors());

const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
});

let isReady = false;

client.on('qr', (qr) => {
  console.log('QR Code received, scan with WhatsApp:');
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ WhatsApp client is ready!');
  isReady = true;
});

client.on('auth_failure', (msg) => {
  console.error('❌ Authentication failed:', msg);
  isReady = false;
});

client.on('disconnected', (reason) => {
  console.log('❌ Client disconnected:', reason);
  isReady = false;
});

client.initialize();

app.post('/send-message', async (req, res) => {
  try {
    if (!isReady) {
      return res.status(503).json({ success: false, error: 'WhatsApp client not ready' });
    }

    const { phoneNumber, message } = req.body;

    if (!phoneNumber || !message) {
      return res.status(400).json({ success: false, error: 'Phone number and message required' });
    }

    // Format: 919750750519 (without +)
    const chatId = phoneNumber.replace(/\D/g, '') + '@c.us';

    await client.sendMessage(chatId, message);

    res.json({ success: true, message: 'Message sent successfully' });
  } catch (error) {
    console.error('Send message error:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.get('/status', (req, res) => {
  res.json({ ready: isReady });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`WhatsApp server running on port ${PORT}`);
});
