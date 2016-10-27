from typing import Tuple

def connect(endpoint: Tuple[str, int, int, int]) -> None:
    a, b, c, d = endpoint

if __name__ == '__main__':
    connect(('1.2.3.4', 1234, 1, 1, 1))