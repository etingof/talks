"""Simple container implementation

Task is to fix programming bugs found by the type checker.
"""
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Node(Generic[T]):
    """Represents sequence node carrying value of abstract type"""
    def __init__(self, initdata: T) -> None:
        self.data = initdata
        self.next: Optional['Node'] = None

    def getData(self) -> T:
        return self.data

    def getNext(self) -> 'Node':
        return self.next

    def setData(self, newdata: T) -> None:
        self.data = newdata

    def setNext(self, newnext: 'Node') -> None:
        self.next = newnext

class UnorderedList(Generic[T]):
    """Represents a sequence of nodes"""
    def __init__(self):
        self.head:Optional['Node'] = None

    def isEmpty(self) -> bool:
        return self.head == None

    def add(self, item: T):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self) -> int:
        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()
        return count

    def search(self, item: T) -> bool:
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def remove(self, item: T) -> None:
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())


if __name__ == '__main__':

    mylist: UnorderedList[int] = UnorderedList()

    mylist.add('31')
    mylist.add(77)
    mylist.add(17)
    mylist.add(93)
    mylist.add(26)
    mylist.add(54.0)

    print(mylist.size())
    print(mylist.search(93))
    print(mylist.search(100))

    mylist.add(100)
    print(mylist.search(100))
    print(mylist.size())

    mylist.remove(54)
    print(mylist.size())
    mylist.remove(93)
    print(mylist.size())
    mylist.remove(31)
    print(mylist.size())
    print(mylist.search(93))
