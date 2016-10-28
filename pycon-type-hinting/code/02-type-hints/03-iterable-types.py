from typing import Iterable

def select_values(d: Iterable, s: str) -> Iterable:
    return [v for v in d if s == v]

# mypy: OK
select_values([1, 2, 3])

# mypy: Argument 1 to "select_values" has incompatible type "int";
#       expected Iterable[Any]
select_values(123, 'x')
