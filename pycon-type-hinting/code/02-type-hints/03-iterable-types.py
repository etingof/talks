from typing import Iterable

def select_values(d: Iterable, s: str) -> Iterable:
    return [v for v in d if s == v]

l: list

# mypy: Incompatible types in assignment (expression has type
#       Iterable[Any], variable has type List[Any])
l = select_values(['x', 'y'], 'x')

# mypy: Argument 1 to "select_values" has incompatible type "int";
#       expected Iterable[Any]
select_values(123, 'x')
