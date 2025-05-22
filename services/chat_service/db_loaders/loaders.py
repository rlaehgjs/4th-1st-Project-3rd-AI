from langchain_core.runnables import RunnableLambda
from services.chat_service.prompts.prompt_input import build_prompt_input
from core.config import summary_collection, chat_collection
from core.constants import MAX_RECENT_LOGS


# 1. 요약 로딩 단계
def fetch_summary(user_id: str) -> str:
    return (summary_collection.find_one({"user_id": user_id}) or {}).get("summary", "")

load_summary = RunnableLambda(lambda x: {
    **x,
    "summary": fetch_summary(x["user_id"])
})

# 2. 최근 대화 로딩 단계
def fetch_recent_chat(user_id: str) -> str:
    logs = list(
        chat_collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(MAX_RECENT_LOGS)
    )[::-1]

    return "\n".join(
        f"{'User' if log['role'] == 'user' else 'AI'}: {log['text']}"
        for log in logs
    )

load_recent_chat = RunnableLambda(lambda x: {
    **x,
    "recent_chat": fetch_recent_chat(x["user_id"])
})

# 3. Prompt input 구성 단계
build_input = RunnableLambda(lambda x: build_prompt_input(
    mbti=x["mbti"],
    input_text=x["input_text"],
    summary=x.get("summary", ""),
    recent_chat=x.get("recent_chat", "")
))

# 4. 전체 input builder 체인
input_builder_chain = load_summary | load_recent_chat | build_input
