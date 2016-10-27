"""
This code will fail at runtime...
Could you help `mypy` catching the problem at compile time?
"""
def sum_up_anything_similar(a, b):
    return a + b

if __name__ == '__main__':
    sum_up_anything_similar(b'x', b'y') + b'z'
    sum_up_anything_similar('x', 'y') + 'z'
    sum_up_anything_similar(1, 2) + 3
    sum_up_anything_similar([1], [2]) + [3]

    # By this moment, the Evil Spirit has planted itself
    # into Programmer's soul and he utterly forgot how to code...
    # Can you save Programmer from failing miserably?
    # (hint: he always runs `mypy` prior to commit)
    sum_up_anything_similar('x', 'y') + 3
    sum_up_anything_similar(1, 2) + 'z'
    sum_up_anything_similar('x', [])
