"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""


def dual_concat(*pairs):
    """Takes any number of tuples (holding str and int objects),
       returns a pair of values
    """
    accumulated_strings = ''
    accumulated_numbers = 0
    for pair in pairs:
        string, number = pair
        accumulated_strings += string
        accumulated_numbers += number << 1

    return accumulated_strings, accumulated_numbers


if __name__ == '__main__':
    c = dual_concat(('a', 1),
                    ('b', 2),
                    # The rest of parameters are buggy.
                    # Can `mypy` catch them?
                    (b'c', 3),
                    (4, 'd'),
                    ('e', 5, 6))
    print(c)
