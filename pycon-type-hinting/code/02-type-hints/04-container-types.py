from typing import Sequence, Mapping

def select_values(d: Mapping, s: str) -> list:
    return [v for k, v in d.items() if s == k]

l: Sequence

# mypy: OK
l = select_values({1: 'x'}, 'x')

# mypy: Argument 1 to "select_values" has incompatible
#       type "str"; expected Mapping[Any, Any]
#       Argument 2 to "select_values" has incompatible type
#       Dict[str, int]; expected "str"
select_values('x', {'x': 1})
