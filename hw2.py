#CSC-364-002
#Dax Henson
#03/26/19
#dch043

'''
rotate left
eg:

p1 = 0b_1100_1111_0011_1111 #org
rotate left
p1 = 0b_1001_1110_0111_1111
'''

from bcpu import *

rotate = """
Set(r0, 0)
Set(r1, 1)
Moven(r0, r1, r4)
Add(r4, r4, r4)
Or(r4, r4, r0)
"""
