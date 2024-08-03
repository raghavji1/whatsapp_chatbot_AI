from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader

# Load environment variables from .env file
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Initialize embeddings model
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Load documents
loader = TextLoader("./data.md")
data = loader.load()

# Initialize Pinecone index
index_name = "jobs"
index = pc.Index(index_name)

# Create Pinecone vector store from documents
docsearch = PineconeVectorStore.from_documents(data, embeddings, index_name=index_name)
