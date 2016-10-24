from typing import List, Dict

def select_values(d: Dict[str, int], s: str) -> List[int]:
    return [v for k, v in d.items() if s == k]

l: List[int]
s: str

l = select_values({1: 'x'}, 'x')  # mypy: List item 0 has incompatible
                                  # type "Tuple[int, str]"

s = select_values({'x': 1}, 'x')  # mypy: Incompatible types in
                                  # assignment (expression has type
                                  # List[int], variable has type "str")