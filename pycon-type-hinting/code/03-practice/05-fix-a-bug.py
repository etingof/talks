"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
from typing import Tuple

Endpoint = Tuple[str, int, int, int]

def connect(e: Endpoint) -> None:
    a, b, c, d = e

if __name__ == '__main__':
    connect(('1.2.3.4', 1234, 1, 1, 1))