from typing import Tuple, Union

def make_dict(*items: Tuple[str, Union[int, str]]) -> dict:
    return dict(items)

if __name__ == '__main__':
    print(make_dict(('x', 1), ('y', 'text') + ('x', 2)))