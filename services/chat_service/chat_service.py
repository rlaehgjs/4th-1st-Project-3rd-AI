from datetime import datetime
from services.chat_service.db_loaders.loaders import input_builder_chain
from services.chat_service.chains.chat_chain import chat_chain
from core.config import logger
from services.chat_service.summary.summary_service import update_summary
import asyncio


async def process_chat(chat_request):
    try:
        # 1. 요약 + 최근 대화 로딩 + input_data 조립 (체인 방식)
        input_data = await input_builder_chain.ainvoke({
            "user_id": str(chat_request.user_id),
            "mbti": chat_request.mbti,
            "input_text": chat_request.input_text
        })

        # 2. 모델 응답 생성 (LangChain 체인 실행)
        response_text = await chat_chain.ainvoke(input_data)

    except Exception as e:
        logger.error(f"[chat_service 오류] {e}")
        response_text = "응답 생성 중 오류가 발생했어요. 다시 시도해줄래요?"

    # 3. 요약 기능 비동기 실행
    now = datetime.utcnow()
    asyncio.create_task(update_summary(
        user_id=str(chat_request.user_id),
        mbti=chat_request.mbti,
        now=now
    ))
    
    # 4. 응답 반환
    return {
        "user_id": chat_request.user_id,
        "mbti": chat_request.mbti,
        "input_text": chat_request.input_text,
        "response": response_text,
        "response_timestamp": datetime.utcnow().isoformat() + "Z"
    }
