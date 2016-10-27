"""Run mypy to find a bug in the following code. Fix the bug.
"""
from typing import Iterator


def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

def prettify_ints(seq: Iterator[int]) -> str:
    return '| '.join(seq)


if __name__ == '__main__':
    print(prettify_ints(fib(22)))
