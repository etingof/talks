from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()
# Continuing
class Job(object):
    """Some job class"""

stack: Stack[Job] = Stack()

stack.push(Job())     # mypy: OK
j: Job = stack.pop()  # mypy: OK
stack.push(123)       # mypy: Argument 1 to "push" of "Stack"
                      #       has incompatible type "int";
                      #       expected "Job"