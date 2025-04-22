from datetime import datetime
from core.config import chat_model, chat_collection, summary_collection, logger
from core.prompt_builder import build_prompt


async def process_chat(chat_request):
    user_id = chat_request.user_id

    # 1. 이전 요약 불러오기
    summary_doc = summary_collection.find_one({"user_id": user_id})
    summary_text = summary_doc["summary"] if summary_doc else ""

    # 2. 최근 대화 10개만 불러오기 (가장 최근 5쌍)
    recent_logs = list(
        chat_collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(10)
    )[::-1]  # 다시 시간순 정렬

    # 3. 최근 대화 원문 구성
    recent_chat_text = ""
    for log in recent_logs:
        role = "User" if log["role"] == "user" else "AI"
        recent_chat_text += f"{role}: {log['text']}\n"

    # 4. 프롬프트 구성 및 GPT 응답 생성
    prompt = build_prompt(
        chat_request.mbti,
        summary_text,
        recent_chat_text,
        chat_request.input_text
    )

    try:
        response = chat_model.invoke(prompt)
        response_text = response.content.strip()
    except Exception as e:
        response_text = "응답 생성 중 오류가 발생했어요. 다시 시도해줄래요?"
        logger.error(f"[GPT 응답 오류] {e}")

    now = datetime.utcnow()

    # 5. 대화 로그 저장
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
        logger.error(f"MongoDB 대화 저장 오류: {db_e}")

    # 6. 응답 저장 이후 전체 대화 재조회 (요약용)
    updated_logs = list(
        chat_collection.find({"user_id": user_id})
        .sort("timestamp", 1)
        .limit(30)
    )

    logs_to_summarize = updated_logs[:-10] if len(updated_logs) > 10 else []

    # 7. 오래된 대화 요약 생성
    if logs_to_summarize:
        text_to_summarize = ""
        for log in logs_to_summarize:
            role = "User" if log["role"] == "user" else "AI"
            text_to_summarize += f"{role}: {log['text']}\n"

        try:
            summary_prompt = f"""다음 대화를 2~3문장으로 요약해줘. 기존 요약과 합쳐도 좋아:

[기존 요약]
{summary_text}

[새로 요약할 대화]
{text_to_summarize}
"""
            summary_response = chat_model.invoke(summary_prompt)
            updated_summary = summary_response.content.strip()
            logger.debug(f"[요약 결과] {updated_summary}")

            summary_collection.update_one(
                {"user_id": user_id},
                {"$set": {
                    "summary": updated_summary,
                    "updated_at": now
                }},
                upsert=True
            )
        except Exception as e:
            logger.error(f"[요약 실패] {e}")
            logger.debug(f"[요약 텍스트] {text_to_summarize}")

    # 8. 응답 반환
    return {
        "user_id": user_id,
        "mbti": chat_request.mbti,
        "input_text": chat_request.input_text,
        "response": response_text,
        "response_timestamp": now.isoformat() + "Z"
    }
