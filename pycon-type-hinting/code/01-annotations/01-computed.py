"""Annotate function with computed value
"""
from datetime import datetime


def foo() -> datetime.now():
    return


if __name__ == '__main__':
    print('Function "{}" instantiated'
    ' at {return}'.format(foo.__name__, **foo.__annotations__))