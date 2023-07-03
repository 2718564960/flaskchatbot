import time
from datetime import datetime
import openai

api_keys = ['sk-0XZzmWvuRBPwbukUrG']

api_key_counts = {key: {'count': 0, 'last_used': None} for key in api_keys}

def get_api_key():
    current_time = time.time()
    for key in api_keys:
        count = api_key_counts[key]['count']
        last_used = api_key_counts[key]['last_used']
        if count < 4 or (count == 4 and current_time - last_used >= 61):
            api_key_counts[key]['count'] += 1
            api_key_counts[key]['last_used'] = current_time
            return key

def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo-0613",
                                 temperature=0.8, max_tokens=500):
    api_key = get_api_key()
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message["content"]


# 使用示例
messages = [
    {"role": "user", "content": "Who won the World Series in 2020?"}
]
for i in range(12):
    print(time.localtime(time.time()))
    completion = get_completion_from_messages(messages)
    print(completion)