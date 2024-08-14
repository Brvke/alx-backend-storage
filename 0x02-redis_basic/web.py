#!/usr/bin/env python3
"""Module for fetching and caching web pages."""
import redis
import requests
from functools import wraps
from typing import Callable


r = redis.Redis()

def cache_with_expiration(expiration: int):
    """Decorator to cache the result of a function in Redis with an expiration time."""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            """Caches the result of the function in Redis."""
            cached_result = r.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            result = method(url)
            r.setex(url, expiration, result)
            return result
        return wrapper
    return decorator

@cache_with_expiration(10)
def get_page(url: str) -> str:
    """Fetches the content of a URL and caches it."""
    # Track how many times a particular URL was accessed
    r.incr(f"count:{url}")

    # Fetch the content of the URL
    response = requests.get(url)
    return response.text
