from bcpu import *

p2 = 4
p3 = 3
p4 = 4
if p2==0:
    p3 = 33
    p4 = 44
else:
    p3 = 30
    p4 = 40
p5 = 55

ifelse = """
Set(r2, 5)
Set(r3, 3)
Set(r4, 4)
Set(r11, 10)
Sub(r12, r11, r2) #if r2 >= 10, r12 will be positive(Rb==0)
Addi(r10, pc, ?endif)
Movep(pc, r10, r12) #if r12 is negative or 0, go to else
    Set(r3, 33)
    Set(r4, 44)
    Addi(pc, pc, ?endelse)
#>endif
    Set(r3, 30)
    Set(r4, 40)
#>endelse
Set(r5, 55)
"""
