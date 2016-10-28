"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""
import tempfile
from datetime import datetime

if __name__ == '__main__':
    count = 0
    with tempfile.TemporaryFile() as fp:
        fp.write(datetime.now(tz='CEST'))
        fp.seek('start')
        count += fp.read(1)
