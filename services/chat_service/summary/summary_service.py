from datetime import datetime
from core.config import chat_collection, summary_collection, logger
from services.chat_service.chains import summary_chain
from core.constants import MAX_RECENT_LOGS, SUMMARY_BUFFER_COUNT


async def update_summary(user_id: str, mbti: str, now: datetime) -> None:
    try:
        # 기존 요약 문서 조회
        existing_summary_doc = summary_collection.find_one({"user_id": user_id})
        last_summary_time = existing_summary_doc.get("updated_at") if existing_summary_doc else None
        previous_summary = existing_summary_doc.get("summary", "") if existing_summary_doc else ""

        # 마지막 요약 시점 이후 로그만 조회
        query = {"user_id": user_id}
        if last_summary_time:
            query["timestamp"] = {"$gt": last_summary_time}

        logs = list(
            chat_collection.find(query)
            .sort("timestamp", 1)
        )

        # 최근 대화는 요약하지 않음
        if len(logs) <= MAX_RECENT_LOGS:
            return

        logs_to_summarize = logs[:-MAX_RECENT_LOGS]

        # 요약할 로그 문자열로 구성
        new_logs_text = "\n".join(
            f"{'User' if log['role'] == 'user' else 'AI'}: {log['text']}"
            for log in logs_to_summarize
        )

        # LangChain 체인 실행
        input_data = {
            "previous_summary": previous_summary.strip(),
            "new_logs": new_logs_text.strip()
        }
        updated_summary = await summary_chain.ainvoke(input_data)

        # 요약 업데이트 저장
        summary_collection.update_one(
            {"_id": f"{user_id}_{mbti}"},
            {"$set": {
                "user_id": user_id,
                "mbti": mbti,
                "summary": updated_summary,
                "updated_at": now
            }},
            upsert=True
        )

        logger.debug(f"[요약 완료] user_id={user_id}")

    except Exception as e:
        logger.error(f"[요약 실패] {e}")
