def count_letters(s: 'input string',
                  l: 'letter to count') -> 'letter counter':
    return s.count(l)

sentence: 'data we work on' = 'Beautiful is better than ugly.'
t_count: 'number of letters found'

t_count = count_letters(sentence, 't')

print('Found {} "t"s in the sentence'.format(t_count))
