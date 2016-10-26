from typing import Tuple

def make_dict(*items: Tuple[str, int]) -> dict:
    return dict(items)

a = make_dict(('x', 1, 2))  # mypy: Argument 1 to "make_dict" has
                            # incompatible type "Tuple[str, int, int]";
                            # expected "Tuple[str, int]"

b = make_dict(['x', 1])     # mypy: Argument 1 to "make_dict" has
                            # incompatible type List[object];
                            # expected "Tuple[str, int]"
# Continuing
from typing import Any

def make_items(**d) -> Tuple[Tuple[str, Any], ...]:
    return tuple(d.items())

c = make_items(x=1, y=2)  # mypy: OK

d = 'x', 1
d = make_items(x=1, y=2)  # mypy: Incompatible types in assignment
                          #       (expression has type
                          #       Tuple[Tuple[str, Any], ...],
                          #       variable has type "Tuple[str, int]")
