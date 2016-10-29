"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
from typing import Tuple

Endpoint = Tuple[str, int, int, int]


def connect(e: Endpoint) -> str:
    a, b, c, d = e
    return 'connected'


if __name__ == '__main__':
    # Game plan:
    # 1. Look closely into mypy reporting
    # 2. Identify issues in code that mypy is complaining on
    # 3. Modify funtion call to make both script and mypy happy
    print(connect(('1.2.3.4', 1234, 1, 1, 1)))
