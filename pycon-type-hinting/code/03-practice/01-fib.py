from typing import Iterator

def fib(n: int) -> Iterator[int]:
    a, b = 0, 1
    while a < n:
        yield a
        a, b = b, a + b

if __name__ == '__main__':
    l: Iterator[int] = list(fib(22))
