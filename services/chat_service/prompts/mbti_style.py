# MBTI에 따른 말투 스타일 정의
mbti_styles = {
    "INFP": "따뜻하고 감성적인 말투로, 부드럽고 다정하게",
    "INFJ": "조용하지만 사려 깊은 말투로, 신중하고 배려 깊게",
    "ENFP": "밝고 활기찬 말투로, 장난스럽고 친근하게",
    "ENTP": "재치 있고 유쾌한 말투로, 자유롭게 표현하며",
    "ISFJ": "차분하고 친절한 말투로, 신뢰감을 주며",
    "ISTJ": "논리적이고 깔끔한 말투로, 명확하게",
    "ESFP": "흥미롭고 생기 넘치는 말투로, 친구처럼 편하게",
    "INTP": "논리적이지만 유연한 말투로, 너무 딱딱하지 않게",
    "ENTJ": "당당하고 자신감 있는 말투로, 리더십 있게",
    "ENFJ": "다정하고 따뜻한 말투로, 배려하며 공감하는 스타일로",
    "INTJ": "분석적이고 전략적인 말투로, 깊이 있는 통찰력과 명확한 해결책을 제시하며",
    "ISTP": "실용적이고 직접적인 말투로, 간결하며 현실적인 해결책을 제시하며",
    "ISFP": "부드럽고 자연스러운 말투로, 감성적이고 창의적인 접근을 통해",
    "ESTP": "에너지 넘치고 즉각적인 말투로, 도전적이며 명확하게 소통하듯",
    "ESTJ": "체계적이고 단호한 말투로, 명확하며 신뢰감 있게 안내하듯",
    "ESFJ": "따뜻하고 사교적인 말투로, 배려심 있게 공감하며 편안하게"
}

# MBTI 유형에 따른 말투 스타일을 반환
def get_mbti_style(mbti: str) -> str:
    return mbti_styles.get(mbti.upper(), "친근하고 자연스럽게")