from fastapi import APIRouter
from models.schema import ChatRequest
from services.chat_service import process_chat

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    return await process_chat(chat_request)
