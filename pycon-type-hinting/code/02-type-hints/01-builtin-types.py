def count_letters(s: str, l: str) -> int:
    return s.count(l)

sentence: str = 'Beautiful is better than ugly.'
t_count: int

# mypy: Argument 2 to "count_letters" has incompatible type
#       "int"; expected "str"
t_count = count_letters(sentence, 123)

# mypy: Incompatible types in assignment (expression
#       has type "int", variable has type "str")
sentence = count_letters(sentence, 't')