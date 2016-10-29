"""
This code will fail at runtime...
Could you use `mypy` to discover the problem at compile time and fix it?
"""


if __name__ == '__main__':
    # Game plan:
    # 1. Look closely into mypy reporting
    # 2. Identify issues in code that mypy is complaining on
    # 3. Modify funtion call to make both script and mypy happy
    count = 0
    with open('/etc/passwd') as f:
        f.seek(0)
        count += len(f.readlines())

    print('Read {} lines'.format(count))
