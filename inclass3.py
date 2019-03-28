from bcpu import *

#while loop

p2 = 0
p3 = 0
while p2 < 10:
    p3 = p3 + p2
    p2 = p2 + 1
print(p3)

#asm

whileloop = """
Set(r2, 0)
Set(r3, 0)
#>while
Addi(r10, pc, ?endwhile)
Subi(r9, r2, 10)
Movep(pc, r10, r9)
    Add(r3, r3, r2)
    Addi(r2, r2, 1)
    Subi(pc, pc, ?while)
#>endwhile
"""

startfast(whileloop)
printi(R[3])
