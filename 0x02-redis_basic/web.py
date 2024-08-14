#!/usr/bin/env python3
"""
Defines the get_page function.
"""


import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()

def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a URL is accessed.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the count for the URL
        count_key = f"count:{url}"
        r.incr(count_key)

        # Retrieve the cached HTML if it exists
        html = r.get(url)
        if html:
            return html.decode("utf-8")

        # Fetch the HTML and cache it
        html = method(url)
        r.set(url, html.encode("utf-8"), ex=10)
        return html

    return wrapper

@count_calls
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
