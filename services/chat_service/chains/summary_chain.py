from services.chat_service.prompts.summary_template import summary_template
from core.config import chat_model
from langchain_core.output_parsers import StrOutputParser

summary_chain = summary_template | chat_model | StrOutputParser()