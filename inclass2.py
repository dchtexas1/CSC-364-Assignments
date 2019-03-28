
"""
p2 = 2
p3 = 3
p4 = 11 if (p2 == 0 and p3 != 0) else 10
print(p4)
"""

from bcpu import *

andfile = """
Set(r2, 2)
Set(r3, 3)

Set(r4, 10)
Set(r5, 11)

Set(r12, 0)
Set(r13, 0)
Set(r1, 1)
Movez(r12, r1, r2)
Movex(r13, r1, r3)
And(r9, r12, r13)
Movex(r4, r5, r9)
"""

#============================

p2 = 2
p3 = 3
p4 = 4
if p2==0:
    p3 = 33
    p4 = 44
p5 = 55


asmfile = """
Set(r2, 2)
Set(r3, 3)
Set(r4, 4)
#if p2==0:
# if p2 != 0 goto endif
Addi(r10, pc, ?endif) #addr of endif
Movex(pc, r10, r2) #goto endif if r2 != 0
    Set(r3, 33)
    Set(r4, 44)
#>endif
Set(r5, 55)
"""
