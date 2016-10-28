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

def sum_ints(numbers: Tuple[int, ...]) -> int:
    return sum(numbers)

sum_ints((1, 2, 3))  # mypy: OK

sum_ints((1, '2'))   # mypy: Argument 1 to "sum_ints" has
                     #       incompatible type "Tuple[int, str]";
                     #       expected Tuple[int, ...]
