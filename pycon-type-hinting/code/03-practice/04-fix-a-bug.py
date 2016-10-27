"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
from typing import Tuple, Union

def make_dict(*items: Tuple[str, Union[int, str]]) -> dict:
    return dict(items)

if __name__ == '__main__':
    print(make_dict(('x', 1), ('y', 'text') + ('x', 2)))