"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""


class Args(object):
    def __init__(self, sentence: str, letter: str) -> None:
        self.sentence = sentence
        self.letter = letter


def count_letters(a: Args) -> int:
    return a.sentence.count(a.letter)


if __name__ == '__main__':
    c = count_letters(
        # Bug in second parameter type. Can `mypy` catch it?
        Args('Beautiful is better than ugly.', 1)
    )
    print('Found {} letters'.format(c))