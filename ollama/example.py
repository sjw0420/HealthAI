import ollama

# Ollama 모델을 사용한 간단한 건강 관련 대화 예제
response = ollama.chat(model='llama3.1', messages=[
    {'role': 'user', 'content': '두통이 있을 때 어떻게 해야 하나요?'},
])

# 챗봇의 응답 출력
print("Bot:", response['message']['content'])
