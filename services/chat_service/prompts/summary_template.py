from langchain.prompts import PromptTemplate

summary_template = PromptTemplate.from_template("""
다음 대화를 2~3문장으로 요약해줘. 기존 요약과 합쳐도 좋아:
[기존 요약]
{previous_summary}
[새로 요약할 대화]
{new_logs}
""")