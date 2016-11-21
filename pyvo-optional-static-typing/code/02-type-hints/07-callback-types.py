from typing import Callable

def callback(msg: str) -> None:
    print('callback called with {}'.format(msg))

def caller(cb_fun: Callable[[str], None]):
    cb_fun('message from caller')

caller(callback)  # mypy: OK

# mypy: Argument 1 to "caller" has incompatible type Callable[
#       [Callable[[str], None]], Any]; expected Callable[[str], None]
caller(caller)
