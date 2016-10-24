i = 1           # Infer type 'int' for i
l = [1, 2]      # Infer type 'list' of 'int's for l

# mypy: Unsupported operand types for + ("int" and List[int])
i += l

# mypy: Argument 1 to "append" of "list" has incompatible
#       type "str"; expected "int"
l.append('xxx')