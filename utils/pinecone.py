from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Pinecone as PineconeStore
from datetime import datetime, date
from langchain_core.messages import AIMessage, HumanMessage
import os

# Pinecone setup
PINECONE_INDEX_NAME = "jobs"
PINECONE_ENVIRONMENT = "gcp-starter"
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def get_vectorstore():
    vector_store = PineconeStore.from_existing_index(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
    return vector_store

def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI(model="gpt-4o")
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain

def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI(model="gpt-4o")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """The following is a friendly conversation between a human and an AI. The AI acts as a recruiter.
        The AI is talkative and asks the user specific details in an interactive way.
        only ask this questions and nothing else.. in the same order.

        1) AI firstly asks the user's full name.
        2) Then the AI asks for the user's expected position.
        3) Then the AI asks for the user's vessel type.
        4) Then the AI asks for the user's salary expectation.
        5) Finally, the AI asks for the user's citizenship.

        The AI ensures to ask one question at a time and waits for the user's response before proceeding to the next question. The AI does not provide any feedback on the availability of positions; it only collects the required information.

        Based on the current conversation history, the AI will determine which questions have already been answered and ask the next appropriate question.
        based on the conversation you will provide the perfect fit jobs in formatted manner, make sure the answer should be relevant as per user need,
        
         
        make sure you are not using any text formatting and link should be one, and more than one open positions are available please provide them,
        the expected answer should be:
        
        1. Position: Chief Engineer
        Vessel Type: General cargo vessel
        Location: Portugal
        Salary: 7200 EUR
        Contract Duration: 3-4 months
        Details: Take over of new-built vessel
        Link: https://www.balticshipping.com/job/16710
        
        make sure you provide one link per position, and do not use dash(-) or bold words
        also use bold to user name like *user_name* when you provide the jobs lastly generate a thank you message for using our services.

        
         
         
         \n\n{context}"""),
        MessagesPlaceholder(variable_name="chat"),
        ("user", "{input}"),
    ])
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

def get_response(user_input, chat, vector_store):
    retriever_chain = get_context_retriever_chain(vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    response = conversation_rag_chain.invoke({
        "chat": chat,
        "input": user_input
    })
    return response['answer']

def load_chat(sender_id, collection):
    session = collection.find_one({"session_id": sender_id})
    if session and "chat" in session:
        return [
            HumanMessage(content=item["user"]) if "user" in item else AIMessage(content=item["ai"]) for item in session["chat"]
        ]
    return []

def save_message_to_mongo(sender_id, user_content, ai_content, collection):
    date_str = str(date.today())
    composite_key = f"{sender_id}_{date_str}"

    message = {
        "user": user_content,
        "ai": ai_content,
        "timestamp": datetime.utcnow()
    }
    collection.update_one(
        {"session_id": composite_key},
        {"$push": {"chat": message}},
        upsert=True
    )

