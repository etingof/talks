"""Accessing annotations at runtime

Facilitates automatic documentation generators.
"""

def count_letters(s: 'input string',
                  l: 'letters to count') -> 'count of letters "l" found':
    return s.count(l)

print('Function "{}"\n'
      'takes {s} and {l},\n'
      'returns {return}'.format(count_letters.__name__,
                                **count_letters.__annotations__)
)
