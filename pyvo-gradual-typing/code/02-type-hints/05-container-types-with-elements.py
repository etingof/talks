from typing import List, Dict

def select_values(d: Dict[str, int], s: str) -> List[int]:
    return [v for k, v in d.items() if s == k]

l: List[int]
s: str

# mypy: OK
l = select_values({'x': 1}, 'x')

# mypy: List item 0 has incompatible type "Tuple[int, str]"
l = select_values({1: 'x'}, 'x')
