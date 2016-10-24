from typing import Generator

def find_substring(pattern) -> Generator[int, str, None]:
    matches = 0
    while True:
        line = (yield matches)
        if pattern in line:
            matches +=1

# Continuing

g = find_substring('b')

next(g)

# mypy: Incompatible types in assignment (expression
#       has type "int", variable has type "bool")
i: bool = g.send('abc')

# mypy: Argument 1 to "send" of "Generator" has incompatible
#       type "bytes"; expected "str"
j: int = g.send(b'def')
