from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder


# LangChain ChatPromptTemplate 구성
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "너는 {mbti} 성격을 가진 AI 챗봇이야. {style} 말투로 이야기해줘. "
               "10~20대와 친구처럼 대화하고, 응답은 3문장 이내로 말해줘."),
    ("system", "예시:\nUser: 기분이 별로야.\nAI: 왜 그래? 무슨 일 있었어??\n"
               "User: 뭐 먹을까?\nAI: 든든한 국밥 어떰?"),
    MessagesPlaceholder(variable_name="messages")
])