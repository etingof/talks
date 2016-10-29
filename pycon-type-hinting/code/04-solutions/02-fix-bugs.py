"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
from typing import Iterator, Callable


def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b


def generate_ints(cb_fun: Callable[[int], Iterator[int]], arg: int) -> str:
    return ', '.join([str(x) for x in cb_fun(arg)])


if __name__ == '__main__':
    # Game plan:
    # 1. Look closely into mypy reporting
    # 2. Identify issues in code that mypy is complaining on
    # 3. Modify funtion call to make both script and mypy happy
    print(generate_ints(fib, 22))
