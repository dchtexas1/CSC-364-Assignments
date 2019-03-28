from bcpu import *

#python
p2 = 2
p1 = 11 if p2 == 0 else 10
print(p1)

#asm
Set(r2, 2)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movez(r1, r6, r2) #r1 = r6 if r2 == 0

#python
p2 = 2
p1 = 11 if p2 != 0 else 10
print(p1)

#asm
Set(r2, 2)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movex(r1, r6, r2) #r1 = r6 if r2 != 0

#python
p2 = -2
p1 = 11 if p2 >= 0 else 10
print(p1)

#asm
Set(r2, 2)
Set(r0, 0)
Sub(r2, r0, r2)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movep(r1, r6, r2) #r1 = r6 if r2 >= 0

#python
p2 = -2
p1 = 11 if p2 < 0 else 10
print(p1)

#asm
Set(r2, 2)
Set(r0, 0)
Sub(r2, r0, r2)
Set(r1, 10) #else value
Set(r6, 11) #true value
Moven(r1, r6, r2) #r1 = r6 if r2 < 0

#compare
#==
#!=
#>=
#<=

#python
p2 = 2
p3 = 3
p1 = 11 if p2 == p3 else 10
print(p1)

#asm
Set(r2, 2)
Set(r3, 3)
Sub(r9, r2, r3)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movez(r1, r6, r9)

#python
p2 = 2
p3 = 3
p1 = 11 if p2 != p3 else 10
print(p1)

#asm
Set(r2, 2)
Set(r3, 3)
Sub(r9, r2, r3)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movex(r1, r6, r9)

#python
p2 = 3
p3 = 3
p1 = 11 if p2 >= p3 else 10
print(p1)

#asm
Set(r2, 3)
Set(r3, 3)
Sub(r9, r2, r3)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movep(r1, r6, r9)

#python
p2 = 3
p3 = 2
p1 = 11 if p2 <= p3 else 10
print(p1)

#asm
Set(r2, 3)
Set(r3, 2)
Sub(r9, r3, r2)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movep(r1, r6, r9)

#python
p2 = 3
p3 = 2
p1 = 11 if p2 < p3 else 10
print(p1)

#asm
Set(r2, 3)
Set(r3, 2)
Sub(r9, r2, r3)
Set(r1, 10) #else value
Set(r6, 11) #true value
Movep(r1, r6, r9)
