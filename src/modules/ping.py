#!/bin/env ./.venv/bin/python3
from ping3 import ping

def ping_host(host: str, count: int = 10):
    responses = []
    for i in range(count):
        result = ping(host, timeout=2)
        if result is None:
            responses.append(f"Request {i+1}: Timed out")
        else:
            responses.append(f"Request {i+1}: {round(result * 1000, 2)} ms")
    return responses