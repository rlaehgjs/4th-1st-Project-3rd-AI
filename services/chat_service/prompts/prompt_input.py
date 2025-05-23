from services.chat_service.prompts.mbti_style import get_mbti_style

def build_prompt_input(mbti: str, input_text: str, summary: str, recent_chat: str) -> dict:
    """
    LangChain 체인에 넘길 입력값을 구성

    Parameters:
        mbti (str): 사용자가 원하는 챗봇의 MBTI
        input_text (str): 현재 사용자 입력
        summary (str): 이전 대화 요약
        recent_chat (str): 최근 대화 원문 (user/AI 형식 텍스트)

    Returns:
        dict: LangChain prompt_template에 사용할 입력값
    """

    messages = []

    if summary:
        messages.append({
            "role": "system",
            "content": f"[요약된 이전 대화]\n{summary.strip()}"
        })

    if recent_chat:
        messages.append({
            "role": "system",
            "content": f"[최근 사용자와의 대화]\n{recent_chat.strip()}"
        })

    messages.append({
        "role": "user",
        "content": input_text.strip()
    })

    return {
        "mbti": mbti,
        "style": get_mbti_style(mbti),
        "messages": messages
    }
