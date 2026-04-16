import functools
import random
import time


'''
Problem Statement: The @retry Decorator
In real-world applications, operations like network requests, database queries, or file downloads can fail temporarily due to glitches.

Your task is to write a custom decorator named @retry that automatically retries a failing function before finally giving up.

Requirements:

The decorator must accept three arguments:

max_retries (int): The maximum number of times to retry the function.

delay (int or float): The number of seconds to wait between retries (you can use time.sleep()).

exceptions (tuple): A tuple of exception classes that should trigger a retry. If a different exception is raised, it should not be caught and should fail immediately.

If the function executes successfully, return its result.

If the function raises one of the specified exceptions, it should wait for delay seconds, print a warning message (e.g., "Retrying in {delay} seconds..."), and try again.

If the function fails max_retries times, it should raise the very last exception it encountered.
'''

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
