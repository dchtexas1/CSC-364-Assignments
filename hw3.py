from bcpu import *

p2 = 0
p3 = 3
p4 = 4
if p2==0:
    p3 = 33
    p4 = 44
else:
    p3 = 30
    p4 = 40
p5 = 55

asmfile = """
Set(r2, 2)
Set(r3, 3)
Set(r4, 4)
Addi(r10, pc, ?endif)
Movex(pc, r10, r2)
    Set(r3, 33)
    Set(r4, 44)
    Addi(r10, pc, ?endelse)
    Move(pc, r10)
#>endif
    Set(r3, 30)
    Set(r4, 40)
#>endelse
Set(r5, 55)
"""
