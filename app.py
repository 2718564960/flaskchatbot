from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
# 导入用于与OpenAI进行API通信的库
import openai

# 创建Flask应用程序
app = Flask(__name__)
app.secret_key = 'your_secret_key_here4'
openai.api_key = 'your_secret_key'
socketio = SocketIO(app)

# 在线用户数
online_users = 0

def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo-0613",
                                 temperature=0.8, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    session['chat_history'] = []  # 清空聊天历史
    session['context_history'] = []
    chat_history = []
    return render_template('index.html', chat_history=chat_history)

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []
    chat_history = session['chat_history']

    if 'context_history' not in session:
        session['context_history'] = []
    context = session['context_history']

    if request.method == 'POST':
        # 增加在线用户数
        global online_users
        online_users += 1

        # 发送在线用户数到前端
        socketio.emit('online_users', {'count': online_users}, namespace='/chat')

        user_input = request.form['user_input']
        chat_history = session['chat_history']
        context = session['context_history']
        chat_history.append(('User', user_input))  # 存储用户输入
        context.append({'role': 'user', 'content': f"{user_input}"})
        print(context)
        response = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': f"{response}"})
        chat_history.append(('AI', response))  # 存储AI回答
        session['chat_history'] = chat_history
        session['context_history'] = context
    return render_template('index.html', chat_history=chat_history)

@app.route('/supportme')
def donate():
    return render_template('supportme.html')

@socketio.on('connect', namespace='/chat')
def test_connect():
    global online_users
    online_users += 1
    emit('online_users', {'count': online_users}, broadcast=True)

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    global online_users
    online_users -= 1
    emit('online_users', {'count': online_users}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
