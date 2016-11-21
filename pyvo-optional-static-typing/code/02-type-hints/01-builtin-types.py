def count_letters(s: str, l: str) -> int:
    return s.count(l)

sentence = 'Beautiful is better than ugly.'
t_count: int

# mypy: OK
t_count = count_letters(sentence, 't')

# mypy: Argument 2 to "count_letters" has incompatible type
#       "int"; expected "str"
t_count = count_letters(sentence, 123)
