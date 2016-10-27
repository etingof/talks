"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""

class Employee(object):
    def work(self):
        print('{} is working...'.format(self.__class__.__name__))

class Manager(Employee):
    def fire(self):
        print('{} fires someone!'.format(self.__class__.__name__))

def work(e):
    e.work()

def fire(e):
    e.fire()

if __name__ == '__main__':
    e = Employee()
    m = Manager()

    work(m)
    work(e)
    fire(m)
    fire(e)  # Something fishy is going on here...
             # Can `mypy` catch that?
