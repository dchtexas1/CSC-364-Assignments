# HW 1
# dch043@latech.edu

from bcpu import *

Set(r4, 444%256)
Seth(r4, 444//256)
Set(r5, 55555%256)
Seth(r5, 55555//256)
Add(r4, r4, r5)
Set(r5, 2111%256)
Seth(r5, 2111//256)
Sub(r4, r4, r5)
Set(r1, 0b11110011)
Seth(r1, 0b11110011)
Set(r2, 0b00001000)
Seth(r2, 0b00001000)
Or(r1, r1, r2)
Set(r2, 0b10011111)
Seth(r2, 0b10011111)
And(r1, r1, r2)
Add(r1, r1, r1)
Add(r1, r1, r1)
printb(R[1])
printb(R[4])
