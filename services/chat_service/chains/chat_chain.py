from langchain_core.output_parsers import StrOutputParser

from services.chat_service.prompts.prompt_template import prompt_template
from core.config import chat_model

# 체인 정의
chat_chain = (
    prompt_template | 
    chat_model | 
    StrOutputParser() # 응답에서 content만 추출해 문자열로 반환하는 출력 파서
)
