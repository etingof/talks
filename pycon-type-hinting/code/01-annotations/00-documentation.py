"""Document function and variables
"""

def count_letters(s: 'input string', l: 'letters to count') -> 'count of letters "l" found':
    return s.count(l)

sentence: 'data we work on' = 'Beautiful is better than ugly.'
t_count: 'number of "t"s found'

t_count = count_letters(sentence, 't')

print('Found {} "t"s in the sentence'.format(t_count))
