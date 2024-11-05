import time
def get_time_cost(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    time_cost = end_time - start_time
    return result, time_cost
