class A(object):
    def fa(self) -> str:
        return 'A'

class B(A):
    def fb(self) -> str:
        return 'B'

a: A
b: B

a = B()  # mypy: OK
b = A()  # mypy: Incompatible types in assignment (expression has
         #       type "A", variable has type "B")

