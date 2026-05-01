"""
Problem Statement: The Robust @retry Decorator
Topic: Advanced Python (Decorators & Error Handling)

Write a parameterized decorator named `retry` that automatically retries a 
failed function.

Requirements:
1. Accept arguments: `max_retries` (default 3), `delay` (default 1), 
   and `exceptions` (default (Exception,)).
2. Return the result immediately if successful.
3. If an exception in the `exceptions` tuple is raised, wait `delay` seconds 
   and try again.
4. If it fails after `max_retries`, allow the last exception to propagate.
5. Preserve original function metadata using `functools.wraps`.
"""

import time
import random
from functools import wraps

def retry(max_retries=3, delay=1, exceptions=(Exception, )):
    # The outer function handles the parameters passed to the decorator
    def decorator(func):

        # @wraps preserves the original function's identity (name, docstring, etc.)
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Loop from 1 up to the maximum number of allowed retries
            for i in range(1, max_retries + 1):
                try:
                    # Attempt to execute the target function; return immediately if successful
                    return func(*args, **kwargs)

                # Only catch the specific exceptions passed into the decorator
                except exceptions as e:
                    # If this is the final attempt, print the failure and re-raise the exception natively
                    if i == max_retries:
                        print(f"🚨 Attempt {i} failed: {e}")
                        raise
                    # If there are retries left, print the wait message and pause execution
                    else:
                        print(f"⏳ Waiting {delay} seconds...")
                        time.sleep(delay)

        return wrapper
    return decorator


@retry(max_retries=3, delay=2, exceptions=(ConnectionError, TimeoutError))
def fetch_data():
    print("Attempting to fetch data...")
    # Simulating a random failure
    if random.choice([True, False]):
        raise ConnectionError("Network is down!")
    return {"status": "success", "data": [1, 2, 3]}

# Test the function
result = fetch_data()
print(result)