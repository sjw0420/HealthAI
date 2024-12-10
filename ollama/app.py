from flask import Flask, request, jsonify, render_template
import ollama

app = Flask(__name__)

# 대화 히스토리 저장
chat_history = []
keytopic = ''

# 사전 정보 로드 함수
def load_txt_data_to_history(file_path='./myfile.txt'):
    global keytopic
    history = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.split(":")[0] == '대표키워드':
                    keytopic = line.split(":")[1].strip()
                else:
                    history.append({'role': 'system', 'content': line.strip()})
    except FileNotFoundError:
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
    return history

# myfile.txt 내용을 히스토리에 추가
chat_history.extend(load_txt_data_to_history())

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/keytopic', methods=['GET'])
def get_keytopic():
    return jsonify({'keytopic': keytopic})

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json.get('message', '').strip()

    # 질문이 비어 있을 경우 처리
    if not user_message:
        return jsonify({'message': "질문을 입력해주세요."})

    # 대표 키워드를 포함하여 사용자 메시지 구성
    user_message = f"{keytopic} 관련 질문입니다: {user_message}"
    chat_history.append({'role': 'user', 'content': user_message})

    try:
        # Ollama 모델에 메시지 전달
        response = ollama.chat(model='llama3.1', messages=chat_history)
        bot_message = response['message']['content']

        # 챗봇 응답을 히스토리에 추가
        chat_history.append({'role': 'assistant', 'content': bot_message})

        # 참고 문구 추가
        bot_message += "\n\n*AI 피드백은 참고용이며, 의학적 진단을 대체하지 않습니다. 심각한 증상이 지속되면 전문가와 상담하세요.*"

        return jsonify({'message': bot_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
