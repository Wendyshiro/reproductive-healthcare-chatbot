from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client as TwilioClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reprohealth.db'
db = SQLAlchemy(app)


class Topic(db.Model):
    __tablename__ = 'topics'
    Topic_Id = db.Column(db.Integer, primary_key=True)
    Topic_name = db.Column(db.String(255))


class Content(db.Model):
    __tablename__ = 'content'
    Content_id = db.Column(db.Integer, primary_key=True)
    Content_type = db.Column(db.String(255))
    Content_data = db.Column(db.Text)
    Topic_id = db.Column(db.Integer, db.ForeignKey('topics.Topic_Id'))


class Query(db.Model):
    __tablename__ = 'queries'
    Query_id = db.Column(db.Integer, primary_key=True)
    Query_text = db.Column(db.Text)
    Timestamp = db.Column(db.DateTime)


class Response(db.Model):
    __tablename__ = 'responses'
    Response_id = db.Column(db.Integer, primary_key=True)
    Response_text = db.Column(db.Text)
    Content_id = db.Column(db.Integer, db.ForeignKey('content.Content_id'))
    Query_id = db.Column(db.Integer, db.ForeignKey('queries.Query_id'))


with app.app_context():
    db.create_all()

TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio authentication token'
TWILIO_PHONE_NUMBER = 'XXXX-XXX-XXX'

DIALOGFLOW_PROJECT_ID = 'your dialogflow project id'

twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def detect_intent_texts(project_id, session_id, text, language_code):
    # Get credentials path from environment variable or use local file
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'reprohealthbot.json')
    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Dialogflow credentials not found at {creds_path}. "
            "Please ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account JSON file."
        )
    
    session_client = dialogflow.SessionsClient.from_service_account_file(creds_path)
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def send_message():
    incoming_msg = request.values.get('Body', '').lower()
    project_id = 'reprohealthbot-ebxb'
    fulfillment_text = detect_intent_texts(project_id, "unique", incoming_msg, 'en')
    resp = MessagingResponse()
    message = resp.message()
    message.body(fulfillment_text)
    return str(resp)


if __name__ == "__main__":

    app.run()

