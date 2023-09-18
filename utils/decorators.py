import time


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Time elapsed: {end - start}")

    return wrapper
