from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.pinecone import *
from utils.twilio_api import send_message
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['Andress']
collection = db['chat_history']

@app.route('/')
def home():
    return 'All is well...'

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['Body']
    sender_id = request.form['From']
    print(f"{message} from {sender_id}")

    vector_store = get_vectorstore()

    chat_history = load_chat(sender_id, collection)
    result = get_response(message, chat_history, vector_store)

    send_message(sender_id, result)

    # Save chat history to MongoDB
    save_message_to_mongo(sender_id, message, result, collection)

    # Return the response from the chat model
    return jsonify({"response": result})

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
