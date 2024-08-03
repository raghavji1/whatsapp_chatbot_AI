
# AI-Powered WhatsApp Chatbot for Recruitment Assistance

Overview

This project is an AI-powered chatbot designed to facilitate recruitment processes through WhatsApp. It interacts with job candidates, collects relevant information, and provides job recommendations using LangChain for conversational AI and Pinecone for vector-based retrieval, integrated with MongoDB for chat history storage.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file


`OPENAI_API_KEY=<your_openai_api_key>`

`PINECONE_API_KEY=<your_pinecone_api_key>`
`PINECONE_INDEX_NAME=<your_pinecone_index_name>`
`PINECONE_ENVIRONMENT=<your_pinecone_environment>`


`TWILIO_ACCOUNT_SID=<your_twilio_account_sid>`
`TWILIO_AUTH_TOKEN=<your_twilio_auth_token>`
`TWILIO_PHONE_NUMBER=<your_twilio_phone_number>`


`MONGODB_URI=<your_mongodb_uri>`


## Key Components
Flask: Web framework managing API endpoints and interactions.
LangChain: Conversational retrieval-augmented generation (RAG) chains.
Pinecone: Vector database for efficient information retrieval.
MongoDB: Storage for chat histories.
Twilio: Communication over WhatsApp.

## Features
Context-Aware Conversations: Maintains chat history and provides relevant responses.
Job Recommendations: Suggests jobs based on user input.
User Information Collection: Gathers and stores candidate details for personalized responses.




## Installation

* Clone the Repository

* Install Dependencies:
    - `python -m venv .venv`
    - `source .venv/bin/activate`  
    - `venv\Scripts\activate`
    - `pip install -r requirements.txt`

* Environment Variables
    - Create a .env file and add Dependencies

* Run the Application
    - first download Ngrok and install it after installation,
        - `ngrok http 5000`
        - `python app.py` or `flask run`

