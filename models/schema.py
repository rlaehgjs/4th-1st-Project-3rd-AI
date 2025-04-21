from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    mbti: str
    input_text: str
