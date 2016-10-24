from typing import Sequence, Mapping

def select_values(d: Mapping, s: str) -> list:
    return [v for k, v in d.items() if s == k]

l: Sequence
s: str

# mypy: OK
l = select_values({1: 'x'}, 'x')

# mypy: Incompatible types in assignment (expression has type
#       Sequence[Any], variable has type "str")
s = select_values({'x': 1}, 'x')
