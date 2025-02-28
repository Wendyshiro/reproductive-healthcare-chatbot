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

TWILIO_ACCOUNT_SID = 'AC359a2083c8b551319a33d6677c4d64d1'
TWILIO_AUTH_TOKEN = '1512d65eeb2c9ccaf50fd1bdf3beb1cf'
TWILIO_PHONE_NUMBER = '+14155238886'

DIALOGFLOW_PROJECT_ID = 'reprohealthbot-ebxb'

twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow. SessionsClient.from_service_account_file(r'C:\Users\Administrator.IT\reprohealthbot\reprohealthbot.json')
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