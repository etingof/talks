from typing import Tuple, Dict

def make_dict(*items: Tuple[str, int]) -> Dict[str, int]:
    return dict(items)

d = make_dict(('x', 1, 2))  # mypy: Argument 1 to "make_dict" has
                            # incompatible type "Tuple[str, int, int]";
                            # expected "Tuple[str, int]"

d = make_dict(['x', 1])     # mypy: Argument 1 to "make_dict" has
                            # incompatible type List[object];
                            # expected "Tuple[str, int]"
