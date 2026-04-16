import functools
import random
import time

# LAYER 1: The Decorator Factory
# This takes your configuration arguments.
def retry(max_retries, delay, exceptions):

    # LAYER 2: The Actual Decorator
    # This receives the function you are decorating (fetch_data_from_server).
    def decorator(func):

        # LAYER 3: The Wrapper
        # This is the function that actually executes when fetch_data_from_server is called.
        # It takes *args and **kwargs so it can wrap functions with ANY signature.
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(max_retries=3, delay=1.5, exceptions=(ConnectionError, TimeoutError))
def fetch_data_from_server():
    print("Fetching data from server...")
    # Simulating a flaky network call
    outcome = random.choice(["success", "timeout", "connection_refused"])

    if outcome == "timeout":
        raise TimeoutError("Server took too long to respond.")
    elif outcome == "connection_refused":
        raise ConnectionError("Server refused the connection.")

    return {"status": 200, "data": "Python is awesome!"} 

# Example usage:
if __name__ == "__main__":
    try:
        result = fetch_data_from_server()
        print("Final Result:", result)
    except Exception as e:
        print("Failed after all retries:", e) 