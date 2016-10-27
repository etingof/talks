"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""

class Mouse(object):
    """Represents a mouse edible by Python"""
    def is_yummy(self):
        return True

class Snake(object):
    """Represents a snake feeding on mice"""
    def feed(self, species):
        print('Yummy!' if species.is_yummy() else 'Foo...')

if __name__ == '__main__':
    snake = Snake()

    snake.feed(Mouse())

    # So far so good, but...
    snake.feed(snake)
    # ...ah, skies are falling but Programmer is firing up
    # his trusty `mypy`. Will it save the world? Depends on you!
    #
    # One last piece of advice... there are many kinds of snakes
    # in the world, each kind of snake prays on specific species.
    # In other words, we know who eats whom, and snakes are
    # generally picky...
    #

