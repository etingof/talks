
@micropython.asm_thumb
def asm_add(r0, r1):
    add(r0, r0, r1)

print(asm_add(1, 2))
