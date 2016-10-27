from typing import Tuple

def make_dict(items: Tuple[Tuple[str, int], ...]) -> dict:
    return dict(items)

if __name__ == '__main__':
    d = make_dict((('x', 1), ('y', '2')))
