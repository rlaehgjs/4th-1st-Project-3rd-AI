from datetime import datetime
from core.config import chat_model, chat_collection, logger
from core.prompt_builder import build_prompt

async def process_chat(chat_request):
    user_id = chat_request.user_id

    # MongoDB에서 최근 20개(질문-답변 10쌍) 대화 가져오기
    chat_logs = list(
        chat_collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(20)
    )[::-1]

    chat_history_text = ""
    for log in chat_logs:
        role = "User" if log["role"] == "user" else "AI"
        chat_history_text += f"{role}: {log['text']}\n"

    prompt = build_prompt(chat_request.mbti, chat_history_text, chat_request.input_text)

    try:
        response = chat_model.invoke(prompt)
        response_text = response.content.strip()
    except Exception as e:
        response_text = "응답 생성 중 오류가 발생했어요. 다시 시도해줄래요?"
        logger.error(f"GPT-4 Error: {e}")

    # 대화 저장
    now = datetime.utcnow()
    try:
        chat_collection.insert_many([
            {
                "user_id": user_id,
                "role": "user",
                "text": chat_request.input_text,
                "timestamp": now
            },
            {
                "user_id": user_id,
                "role": "bot",
                "text": response_text,
                "timestamp": now
            }
        ])
    except Exception as db_e:
        logger.error(f"MongoDB Insert Error: {db_e}")

    return {
        "user_id": user_id,
        "mbti": chat_request.mbti,
        "input_text": chat_request.input_text,
        "response": response_text,
        "response_timestamp": datetime.utcnow().isoformat() + "Z"
    }
