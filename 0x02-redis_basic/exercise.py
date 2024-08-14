#!/usr/bin/env python3
""" Cache class for storing data in Redis with additional functionalities """
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments the count each time the method is called."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Stores input and output history in Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)

        return output
    return wrapper

def replay(method: Callable) -> None:
    """Displays the history of calls for a particular function."""
    r = redis.Redis()
    func_name = method.__qualname__
    
    inputs = r.lrange(f"{func_name}:inputs", 0, -1)
    outputs = r.lrange(f"{func_name}:outputs", 0, -1)
    
    print(f"{func_name} was called {len(inputs)} times:")
    for inp, outp in zip(inputs, outputs):
        print(f"{func_name}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")

class Cache:
    """Cache class for storing data in Redis."""
    
    def __init__(self):
        """Initializes a new Cache instance and flushes the Redis database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns the generated key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, int]]] = None) -> Union[str, int, bytes, None]:
        """Retrieves data from Redis and applies an optional conversion function."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieves data from Redis and converts it to a string."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves data from Redis and converts it to an integer."""
        return self.get(key, int)
