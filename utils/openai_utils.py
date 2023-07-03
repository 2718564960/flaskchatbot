import time
from datetime import datetime
import openai

class OpenAIUtils:
    api_keys = ['sk-0XZzmWvuRBPwbukUrGF']
    api_key_usage = {key: {'count': 0, 'last_used': 0} for key in api_keys}
    wait_time = 61

    @staticmethod
    def init(api_keys):
        api_keys = ['sk-0XZzmWvuRB']
        OpenAIUtils.api_keys = api_keys
        OpenAIUtils.api_key_usage = {key: {'count': 0, 'last_used': 0} for key in api_keys}
        print(OpenAIUtils.api_key_usage)

    @staticmethod
    def get_wait_time(api_key):
        current_time = datetime.now()
        last_used_time = OpenAIUtils.api_key_usage[api_key]['last_used']
        if last_used_time is None:
            return 0
        time_difference = current_time - last_used_time
        wait_time = OpenAIUtils.wait_time - time_difference.total_seconds()
        return max(wait_time, 0)

    @staticmethod
    def get_completion_from_messages(messages, model="gpt-3.5-turbo-0613",
                                     temperature=0.8, max_tokens=500):
        for api_key in OpenAIUtils.api_keys:
            wait_time = OpenAIUtils.get_wait_time(api_key)
            if wait_time > 0:
                print(f"Waiting for {wait_time} seconds before using {api_key}")
                time.sleep(wait_time)

            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            OpenAIUtils.api_key_usage[api_key]['count'] += 1
            OpenAIUtils.api_key_usage[api_key]['last_used'] = datetime.now()

            if response.choices[0].message["role"] == "assistant":
                return response.choices[0].message["content"]

        return None


    @staticmethod
    def get_completion(messages):
        return OpenAIUtils.get_completion_from_messages(messages)

if __name__ == '__main__':
    # 使用示例
    messages = [
        {"role": "user", "content": "Who won the World Series in 2020?"}
    ]
    for i in range(12):
        print(time.localtime(time.time()))
        completion = OpenAIUtils.get_completion(messages)
        print(completion)