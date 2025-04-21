import os
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import logging

load_dotenv()

# 환경 변수
openai_api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# GPT 모델
chat_model = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.3,
    openai_api_key=openai_api_key
)

# MongoDB
client = MongoClient(mongo_uri)
db = client["chat_db"]
chat_collection = db["chat_logs"]

# 로깅
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
