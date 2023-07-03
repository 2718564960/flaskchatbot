import time
def calculate_response_time(current_time, time_list_history=[], interval_time=60, threshold=3):
    if len(time_list_history) > threshold:
        raise ValueError(f"列表长度超过{threshold}")
    if len(time_list_history) == 0:
        return True, [current_time], 0
    if current_time - time_list_history[len(time_list_history)-1] > interval_time:
        return True, [current_time], 0
    elif len(time_list_history) < threshold:
        time_list_history[len(time_list_history)] = current_time
        return True, time_list_history, 0
    if len(time_list_history) == threshold:
        if current_time - time_list_history[0] > interval_time:
            time_list_history.pop(0)
            time_list_history.append(current_time)
            return True, time_list_history, 0
        else:
            wait_time = current_time - time_list_history[0]
            time_list_history.pop(0)
            time_list_history.append(current_time)
            return False, time_list_history, wait_time


time_list_history = [1688377616,1688377617,1688377618]


print(calculate_response_time(1688377650,time_list_history))