i = 1             # Infer type 'int' for i
l = [1, 2]        # Infer type 'list' of 'int's for l

i += l            # mypy: Unsupported operand types for +
                  #       ("int" and List[int])

i = 'text'        # mypy: Incompatible types in assignment (expression
                  #       has type"str", variable has type "int")

l.append('text')  # mypy: Argument 1 to "append" of "list" has
                  #       incompatible type "str"; expected "int"
