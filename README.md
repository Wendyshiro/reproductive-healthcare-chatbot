# 💬 WhatsApp Chatbot for Adolescent Reproductive Healthcare

This Flask-based WhatsApp chatbot provides accessible and confidential reproductive health information for adolescents. It uses **Twilio** for WhatsApp integration and **Dialogflow** for natural language understanding.

---

## 🚀 Features
- AI-driven Q&A on reproductive health topics  
- Twilio WhatsApp integration  
- Dialogflow NLP for contextual understanding  
- Scalable, lightweight Flask backend  
- Secure environment variable configuration  

---

## 🧰 Tech Stack
- **Python** (Flask)
- **Twilio API**
- **Dialogflow**
- **ngrok** (for local tunneling)
- **dotenv**

---

## 🧪 Local Setup

### 1️⃣ Clone the Repository
```bash

git clone https://github.com/Wendyshiro/whatsapp-chatbot.git

cd whatsapp-chatbot

2 Clone the Repository

pip install -r requirements.txt

3. Set up Ennvironment

Create a .env file and in your Twilio and Dialogflow credentials

4. Run the app

python index.py

Your Flask app should be live on:

http://localhost:5000

5. Expose with ngrok

ngrok http 5000

Cpy the HTTPS URL and paste it in your Twilio Sandbox Configuration and 

also in The Dialogflow fulfilment webhook

🩺 Potential Use Cases

Health education for teens and young adults

Anonymous and safe Q&A

Integration with digital clinics or telemedicine systems

🧠 Author

Wendy Wanjiru
AI & Software Developer | Focused on Human-Centered Digital Health

