"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""
from collections import defaultdict
from typing import Dict


def aggreggate_dicts(*dicts: Dict[str, int]):
    """Takes a sequence of dicts having string key and integer value.
       Returns sums of values aggreggated by keys
    """
    aggregate: Dict[str, int] = defaultdict(int)
    for d in dicts:
        for k, v in d.items():
            aggregate[k] += v
    return aggregate


if __name__ == '__main__':
    d = aggreggate_dicts(
        {'apples': 123, 'oranges': 456},
        # could you catch the following bugs with `mypy`?
        {'apples': 123, 'oranges': 456},
    )
    print(d)
