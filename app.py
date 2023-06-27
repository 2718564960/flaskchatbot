from flask import Flask, render_template, request, session

# 导入用于与OpenAI进行API通信的库
import openai

# 创建Flask应用程序
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
openai.api_key = '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'
# chat_history = []  # 用于存储用户输入和回答的聊天历史


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]


@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []
    chat_history = session['chat_history']

    if 'context_history' not in session:
        session['context_history'] = [{'role': 'system', 'content': 'You are friendly chatbot.'}]
    context = session['context_history']

    if request.method == 'POST':
        user_input = request.form['user_input']
        chat_history = session['chat_history']
        context = session['context_history']
        chat_history.append(('User', user_input))  # 存储用户输入
        context.append({'role': 'user', 'content': f"{user_input}"})
        response = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': f"{response}"})
        chat_history.append(('AI', response))  # 存储AI回答
        session['chat_history'] = chat_history
        session['context_history'] = context
        print(session['chat_history'])

    if request.method == 'POST' and 'clear_history' in request.form:  # 如果清空历史按钮被点击
        session['chat_history'] = []  # 清空聊天历史
        session['context_history'] = [{'role': 'system', 'content': 'You are friendly chatbot.'}]
        print(session['chat_history'])
        return render_template('index.html', chat_history=[])

    return render_template('index.html', chat_history=chat_history)


if __name__ == '__main__':
    app.run(debug=True)
