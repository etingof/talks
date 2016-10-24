from typing import TypeVar

T = TypeVar('T')             # Type variable denoting opaque type

def make_a_copy(x: T) -> T:  # Generic function
    return x

a: int = make_a_copy(123)    # mypy: OK
b: str = make_a_copy('xxx')  # mypy: OK
c: str = make_a_copy([1])    # mypy: Incompatible types in assignment (expression
                             #       has type List[int], variable has type "str")
# Continuing
N = TypeVar('N', str, bytes)  # Type variable denoting either of types

def concat(x: N, y: N) -> N:  # Generic function
    return x+y

concat('a', 'b')    # mypy: OK
concat(b'a', b'b')  # mypy: OK
concat('a', b'b')   # mypy: Type argument 1 of "concat" has incompatible
                    #       value "object"