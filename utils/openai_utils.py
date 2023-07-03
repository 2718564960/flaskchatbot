import time
from datetime import datetime
import openai

class Robot:
    def __init__(self, api_key):
        self._api_key = api_key
        self._time_list_history = []

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, new_api_key):
        self._api_key = new_api_key

    @property
    def time_list_history(self):
        return self._time_list_history

    @time_list_history.setter
    def time_list_history(self, new_time_list):
        self._time_list_history = new_time_list


class OpenAIUtils:
    api_keys = ['sk-0XZzmWvuRBPwbu']
    robots = [Robot(api_key) for api_key in api_keys]
    robots_num = len(robots)
    current_robot_index = 0
    @staticmethod
    def calculate_response_time(current_time, time_list_history=[], interval_time=60, threshold=3):
        if len(time_list_history) > threshold:
            raise ValueError(f"列表长度超过{threshold}")
        if len(time_list_history) == 0:
            return True, [current_time], 0
        if current_time - time_list_history[-1] > interval_time:
            return True, [current_time], 0
        elif len(time_list_history) < threshold:
            time_list_history.append(current_time)
            return True, time_list_history, 0
        if len(time_list_history) == threshold:
            if current_time - time_list_history[0] > interval_time:
                time_list_history.pop(0)
                time_list_history.append(current_time)
                return True, time_list_history, 0
            else:
                wait_time = 60 - (current_time - time_list_history[0])
                time_list_history.pop(0)
                time_list_history.append(current_time)
                return False, time_list_history, wait_time

    @staticmethod
    def get_robot_api_key():
        time_list_history = OpenAIUtils.robots[OpenAIUtils.current_robot_index].time_list_history
        api_key = OpenAIUtils.robots[OpenAIUtils.current_robot_index].api_key
        can_answer, new_time_list, wait_time = OpenAIUtils.calculate_response_time(time.time(),time_list_history)
        OpenAIUtils.robots[OpenAIUtils.current_robot_index].time_list_history = new_time_list
        time.sleep(wait_time)
        OpenAIUtils.current_robot_index = (OpenAIUtils.current_robot_index + 1) % (OpenAIUtils.robots_num)
        return api_key

    @staticmethod
    def get_completion_from_messages(messages,
                                     model="gpt-3.5-turbo-0613",
                                     temperature=0.8, max_tokens=500):
        api_key = OpenAIUtils.get_robot_api_key()
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"]

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