"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
from typing import Tuple, Union


def make_dict(*items: Tuple[str, Union[int, str]]) -> dict:
    return dict(items)


if __name__ == '__main__':
    # Game plan:
    # 1. Look closely into mypy reporting
    # 2. Identify issues in code that mypy is complaining on
    # 3. Modify funtion call to make both script and mypy happy
    print(make_dict(('x', 1), ('y', 'text'), ('z', 'data'), ('z', '')))