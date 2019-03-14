"""
# BCPU (C) Pr Ben Choi
# Building CPU Simulator:
# 	Code, Load, Run
# 	BCPU asm program

# *** Coding BCPU asm program ***
# A BCPU asm file is a multi-line string defined in py file
# ASM buildin formats allow 3 types of labels in an asm file:

# (1) Define var using #:name = value
# Replace 'name' with 'value', eg:
	#:counter = r6  #create var counter
	#:one = 1
	Addi(counter, counter, one)

# (2) Define label using #>name
# Replace ?name using value of relative offset, eg:
	Set(counter, 15)
	#>while counter >= 0:
	Addi(r10, pc, ?endwhile) # setup jump relative addr
	Moven(pc, r10, counter) # goto >endwhile if counter < 0
  	# whilepart
  	Subi(counter, counter, 1)
  	Subi(pc, pc, ?while) # go back >while
	#>endwhile

# Define function name using #>funcname
#>funcname(...): # define label 'funcname'
  # funcpart
  # ...
  # return using:
  Load(r13, st) # pop return addr
  Subi(st, st, 1) # update stack pointer
  Move(pc, r13) # return back to caller

# call function define in the same file
# from main() call funcname() def before main()
# before calling need to
# push return addr
  Addi(r13, pc, ?returnaddr) # setup relative return addr
  Addi(st, st, 1) # update stack pointer
  Store(st, r13) # push
# calling funcname()
  Set(r13, ?funcname + 1) # relative to next instruction so +1
  Sub(r13, pc, r13) #upward relatve addr
  Move(pc, r13)
  #>returnaddr

# (3) Define the main function name of a file
# by using the first #> label in the file, eg:
# In a file called mullib.py
#>mul(r2, r2)->r4 # the very first asm label in the file
	# ...
  # return
# The name 'mul' is defined
# by load() for compiling and loading asm into memory

# call function def in other file, eg:
# import the file, eg:
	from mullib import *
# ...
# calling 'mul'
	Set(r13, ?mul % 256) # absolute addr of the loaded 'mul'
	Seth(r13, ?mul // 256)
	Move(pc, r13)

# *** Loading asm file ***
# Asm file is compiled and loaded into memory, eg
	load(muldef) # where muldef is a multi-line string containing the asm program
# auto allocate memory for multiple loads, eg
	load(file1)
  load(file2)
# define main function name during load, eg
	load(muldef, fname="multify")

# *** Running asm program ***
	run() # auto use just loaded
	run('func') # run the specific loaded func
  runfast() # run without printing each step

"""
VER = '3.7.8'

# constants (reserved)
H = 0b1111111111111111  # 16 bits
B15 = 0b1000000000000000 # sign bit
Err = -1
PRI = True # printi or not

# register address (reserved const)
R0 = r0 = 0
R1 = r1 = 1
R2 = r2 = 2
R3 = r3 = 3
R4 = r4 = 4
R5 = r5 = 5
R6 = r6 = 6
R7 = r7 = 7
R8 = r8 = 8
R9 = r9 = 9
R10 = r10 = 10
R11 = r11 = 11
R12 = r12 = 12
R13 = r13 = 13
R14 = r14 = 14
PC = Pc = pc = 15 # program counter

# Registers
R = [0 for _ in range(2**4)]

# Data storage
D = [0 for _ in range(2**8)]

# Instruction memory
M = [0 for _ in range(2**16)]


# BIOS ===

# stack
ST = St = st = R14 # stack top
R[st] = 0 # empty
D[0] = 0
"""
# empty if R[st] == 0
# start at D[1] upward
# push:
  Addi(st, st, 1)
  Store(st, r2)
# pop:
  Load(r3, st)
  Subi(st, st, 1)
"""

# data storage I/O address
Di0 = di0 = 210
Di1 = di1 = 211
Di2 = di2 = 212
Di3 = di3 = 213

Do0 = do0 = 220
Do1 = do1 = 221
Do2 = do2 = 222
Do3 = do3 = 223
#

# simulator functions ===

# printing interger + - number
def printi(d,a='',b=''):
  """Print a 16-bit integer"""
  if not PRI: return # not print
  if d&B15: d = -(-d&H)
  if (a != '') and a&B15: a = -(-a&H)
  if (b != '') and b&B15: b = -(-b&H)
  print(d,a,b)

# get interger + - number, out of 16 bits
def geti(b):
  """Get a 16-bit int value"""
  n = b
  if b&B15: n = -(-b&H) # bit15 is sign bit
  return n

# printing a 16-bit binary number
def printb(n):
  """Print 16 bits"""
  ns = '0000000000000000'+bin(n)[2:]
  print(ns[-16:-12], ns[-12:-8], ns[-8:-4], ns[-4:])

# get 16 bits out of + - number
def getb(n):
  """Get 16 bits"""
  b = n&H
  return b


# Instructions 16 defs ===
OPNAMES = ['Move', 'Not', 'And', 'Or',
           'Add', 'Sub', 'Addi', 'Subi',
           'Set', 'Seth', 'Store', 'Load',
           'Movez', 'Movex', 'Movep', 'Moven']

def Move(Rd,Ra):
  """ Rd = Ra """
  vRa = R[Ra]
  R[Rd] = R[Ra]
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa)

def Not(Rd,Ra):
  """ Rd = ~Ra """
  vRa = R[Ra]
  R[Rd] = (~R[Ra])&H
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa)

def And(Rd,Ra,Rb):
  """ Rd = Ra & Rb """
  vRa, vRb = R[Ra], R[Rb]
  R[Rd] = R[Ra] & R[Rb]
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Or(Rd,Ra,Rb):
  """ Rd = Ra | Rb """
  vRa, vRb = R[Ra], R[Rb]
  R[Rd] = R[Ra] | R[Rb]
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Add(Rd,Ra,Rb):
  """ Rd = Ra + Rb """
  vRa, vRb = R[Ra], R[Rb]
  R[Rd] = (R[Ra] + R[Rb])&H
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Sub(Rd,Ra,Rb):
  """ Rd = Ra - Rb"""
  vRa, vRb = R[Ra], R[Rb]
  R[Rd] = (R[Ra] + (-R[Rb])&H)&H
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Addi(Rd,Ra,v):
  """ Rd = Ra + v """
  if not (v>=0 and v<=15):
    print("Value should be 0...15")
    return Err
  vRa = R[Ra]
  R[Rd] = (R[Ra] + v)&H
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, v)

def Subi(Rd,Ra,v):
  """ Rd = Ra - v """
  if not (v>=0 and v<=15):
    print("Value should be 0...15")
    return Err
  vRa = R[Ra]
  R[Rd] = (R[Ra] - v)&H
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa, v)

def Set(Rd,v):
  """ Rd = v """
  if not (v>=0 and v<=255):
    print("Value should be 0...255")
    return Err
  R[Rd] = v
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], v)

def Seth(Rd,v):
  """ Rd = v*256 + Rd%256 """
  if not (v>=0 and v<=255):
    print("Value should be 0...255")
    return Err
  R[Rd] = v*256 + R[Rd]%256
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], v)

def Store(Rd,Ra):
  """ D[Rd] = Ra """
  a = R[Rd]%256
  D[a] = R[Ra]
  R[Pc] += 1
  printi(R[Rd],R[Ra])

def Load(Rd,Ra):
  """ Rd = D[Ra] """
  vRa = R[Ra]
  a = R[Ra]%256
  R[Rd] = D[a]
  if Rd != Pc: R[Pc] += 1
  printi(R[Rd], vRa)

def Movez(Rd,Ra,Rb):
  """ Rd = Ra if Rb == 0 """
  vRa, vRb = R[Ra], R[Rb]
  if R[Rb] == 0:
    R[Rd] = R[Ra]
    if Rd != Pc: R[Pc] += 1
  else:
    R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Movex(Rd,Ra,Rb):
  """ Rd = Ra if Rb != 0 """
  vRa, vRb = R[Ra], R[Rb]
  if R[Rb] != 0:
    R[Rd] = R[Ra]
    if Rd != Pc: R[Pc] += 1
  else:
    R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Movep(Rd,Ra,Rb):
  """ Rd = Ra if Rb >= 0 """
  vRa, vRb = R[Ra], R[Rb]
  if R[Rb]&B15 == 0:
    R[Rd] = R[Ra]
    if Rd != Pc: R[Pc] += 1
  else:
    R[Pc] += 1
  printi(R[Rd], vRa, vRb)

def Moven(Rd,Ra,Rb):
  """ Rd = Ra if Rb < 0 """
  vRa, vRb = R[Ra], R[Rb]
  if R[Rb]&B15:
    R[Rd] = R[Ra]
    if Rd != Pc: R[Pc] += 1
  else:
    R[Pc] += 1
  printi(R[Rd], vRa, vRb)


# os ===

# pre def Addr
class Addr:
  pass
"""
# lib function def as, eg
# first in lib function file, eg mul file
#>mul(r2,r3)->r4: # the top label of a file def func name
  # ...
# last in mul func file
load(mul)

# from main file, call the func
  Set(r10, ?mul % 256)
  Set(r10, ?mul // 256)
  Move(pc, r10)
"""

# memory management
PROGMEM0 = 100 # prog mem start at and up
Addr.justloaded = PROGMEM0 # the prog just loaded (Addr. needed for multi files)
memmap = {} # 'fname':(addrbeg, addrend)
"""
# auto allocate memory for muliple loads, eg
load(mul) # auto find func name from top label
load(div)
load(main)
# run just loaded
run()
# run mul
run('mul') # or
run(Addr.mul) # auto defined addr for mul func
"""

# os process ===

def printr():
  """Print registers"""
  for i in range(15):
    n = R[i]
    if n&B15: n= -(-n&H)
    print('R'+str(i)+':',n)
  print('PC:', R[pc])

def printrb():
  """Print registers bitwise"""
  for i in range(15):
    print('R'+str(i)+':',end=' ')
    printb(R[i])
  print('PC:', end=' ')
  printb(R[pc])

def printd(a=0, z=256):
  """Print data storage"""
  print('D:', end=' ')
  for n in D[a:z]:
    if n&B15: n= -(-n&H)
    print(n, end=', ')
  print()

def printm(a=None):
  """Print memory"""
  a = Addr.justloaded if a==None else a
  while M[a] != 0: # 0 no instuction
    print(M[a], '['+str(a)+']')
    a += 1

def run(a=None):
  """Run program """
  a = Addr.justloaded if a==None else a
  if type(a)==str:
    if a in vars(Addr):
      a = vars(Addr)[a]
    else:
      print(f"*** Run stopped: {a} not loaded")
      return Err
  R[Pc] = a
  while M[a] != 0: # 0 no instuction
    print(M[a], '['+str(a)+']')
    ret = eval(M[a])
    if ret == Err:
      print("*** Run stopped due to above error ***")
      break
    a = R[Pc]

def runfast(a=None, maxi=123000):
  """Run program, not printi, with limit"""
  a = Addr.justloaded if a==None else a
  if type(a)==str:
    if a in vars(Addr):
      a = vars(Addr)[a]
    else:
      print(f"*** Runfast stopped: {a} not loaded")
      return Err
  global PRI
  PRI = False # not printi
  print('*** Running fast, no trace ***')
  mx = 0
  R[Pc] = a
  while M[a] != 0: # 0 no instuction
    try:
      ret = eval(M[a])
    except:
      print(M[a], '['+str(a)+']')
      print("*Err: Asm code syntax error")
      break
    if ret == Err:
      print("*Err: Run stopped due to above error")
      break
    a = R[Pc]
    # run limit in case infinite loop
    mx += 1
    if mx > maxi:
      print("*Err: Run stopped at limit", maxi)
      print("*Err: May due to infinite loop")
      break
  print(f"  * Done in {mx} steps *")
  PRI = True # printi resume
  return mx

def bcompile(ps):
  """Translating program into instructions"""
  # program format:
  # (1) label: #>name
  # replaceement of offset: ?name
  # else (2) replace ?name with value of pre def Addr.name
  # (3) label #:name = value replace name with value

  # auto define function name
  fname = 'main' # default fn name

  pl = ps.splitlines()
  pl = [s.strip() for s in pl]
  pl = [s for s in pl if s != '']

  # create labal dict for #:name = value
  vt0 = [s for s in pl if s[:2] == '#:']
  for s in vt0:
    if '=' not in s:
      print(s)
      print("*** Compile Stop: missing = sign ***")
      return Err
  vt = [s.split(sep='=', maxsplit=2) for s in vt0]
  vt = [(k.strip()[2:],v) for [k,v] in vt]
  vt = [(k,v.split(sep='#', maxsplit=2)[0].strip()) for (k,v) in vt]
  for i in range(len(vt)):
    if vt[i][1] == '':
      print(vt0[i])
      print("*** Compile Stop: missing value ***")
      return Err
  vt = dict(vt)

  # keep #> lines remove rest # lines
  for i in range(len(pl)): #keep #> line
    if pl[i][:2] == '#>':
      pl[i] = '_' + pl[i]
  pl = [s for s in pl if s[0] != '#']

  # create label dict for #>name
  st = []
  for _ in range(len(pl[:])):
    for i in range(len(pl)):
      if pl[i][0] == '_':
        slb = pl[i].split()[0][3:]
        lb = ''
        for s in slb:
          if s.isalnum(): lb += s
          else: break
        st += [(lb, i)]
        # get fn name as the top label
        fname = lb if i==0 else fname
        del pl[i]
        break
  st = dict(st)

  # fix line with ?name
  # ***(? is now reserved keyword)
  for i in range(len(pl[:])):
    if '?' in pl[i]:
      sl = pl[i].split('?')
      lb = ''
      for s in sl[1]: # fix only 1st ?
        if s.isalnum(): lb += s
        else: break
      if lb in st.keys():
        lbv = abs(st[lb] - i) # label relative offset
      elif lb in vars(Addr):
        lbv = vars(Addr)[lb] # pre def label, absolute addr
      else:
        print(f'*** Compile Stop: Label for ?{lb} not found ***')
        return Err
      sl[1] = sl[1].replace(lb, str(lbv), 1)
      pl[i] = ''.join(sl)

  # replace name with value from #:name
  for i in range(len(pl[:])):
    if '(' not in pl[i]:
      print(pl[i])
      print(f'*** Compile Stop: ( not found ***')
      return Err
    sp = pl[i].split(sep='(', maxsplit=2)
    fn = sp[0] # function name
    opname = fn.strip()
    if opname not in OPNAMES:
      print(pl[i])
      print(f'*** Compile Stop: Function is not an ASM operation ***')
      return Err
    if ')' not in sp[1]:
      print(pl[i])
      print(f'*** Compile Stop: ) not found ***')
      return Err
    sp = sp[1].split(sep=')', maxsplit=2)
    rest = sp[1]
    args0 = sp[0]
    args = ''
    for c in args0:
      c = c if c.isalnum() else ' '
      args += c
    args = args.split()
    args = [s.strip() for s in args]
    args = set(args)
    args = list(args)
    args = sorted(args, key=len, reverse=True)
    args1 = args0
    for name in args:
      if name in vt.keys():
        value = vt[name]
        args1 = args1.replace(name, value)
    pl[i] = fn + '(' + args1 + ')' + rest
  ##
  return fname, pl

def allocate(fname, flen, addr)->'addr':
  """Finding a location for loading program"""
  # find slot in memmap to load func
  # update memmap with loaded func
  # auto define Addr.{fname} = {addr}

  global memmap # PROGMEM0, Addr.
  # remove conflict
  if fname in memmap:
    print("*Replacing memory with new code:", fname)
    del memmap[fname]
  # force into addr space
  if addr != None:
    # check conflict
    fr = (addr, addr+flen)
    for k in memmap:
      mv = memmap[k]
      if (mv[0] <= fr[0] <= mv[1]) or (mv[0] <= fr[1] <= mv[1]):
        print(f"*** Addr {addr} conflit with loaded code: {k}")
        print("  * Try giving a higher address")
        return Err
    # free to add
    memmap.update({fname:(addr, addr+flen)})
    exec(f'Addr.{fname} = {addr}')
    return addr
  # find a space to fit prog
  # empty case
  if memmap == {}:
    addr = PROGMEM0
    memmap.update({fname:(addr, addr+flen)})
    exec(f'Addr.{fname} = {addr}')
    return addr
  # check memmap for slot
  mmv = list(memmap.values())
  mmv += [(0, PROGMEM0-1), (2**16-1, 2**16-1)]
  mmv = sorted(mmv)
  for i in range(len(mmv)-1):
    if (mmv[i+1][0] - mmv[i][1]) > (flen+1): # adde 1 for 0 end
      addr = mmv[i][1] + 1
      memmap.update({fname:(addr, addr+flen)})
      exec(f'Addr.{fname} = {addr}')
      return addr
  #
  return Err

def load(ps, addr=None, fname=None):
  """Loading asm codes in memory"""
  # (1) compile
  # (2) allocate
  # (3) load

  bret = bcompile(ps)
  if bret == Err:
    print("*** Load Stop: Compile error ***")
    return Err
  (fname0, pl) = bret

  fname = fname0 if fname == None else fname
  flen = len(pl)
  # allocate mem
  addr = allocate(fname, flen, addr)
  if addr == Err:
    print("*** Load Stop: Cannot Allocate memory ***")
    return Err

  Addr.justloaded = addr
  # load to memory
  a0 = a = addr
  for s in pl:
    M[a] = s
    a += 1
  M[a] = 0 # end

  print("*** Loaded in memory:", (a0,a))
  print("  * Function name is:", fname)
  return (fname, (a0, a)) # allowing load after this addr

def start(asm):
  """Load and Start running the aam code"""
  rc = load(asm)
  if rc != Err:
    run()

def startfast(asm):
  """Load and Start fast running the aam code"""
  rc = load(asm)
  if rc != Err:
    runfast()

# ready
print(f"*** BCPU {VER} startup completed ***")


# testing ===

testprog = """

Set(R1,7)

# logical operation
Move(R2, R1)  # R2=R1
Not(R3, R2) # R3=NOT(R2)
And(R4, R1, R1) # R4= R1 AND R1
Or(R5, R3, R4) # R5 = R3 OR R4

  # arithmetic operation
  Add(R7, R1, R1) # R7=R1+R1
  Sub(R8, R7, R2) # R8 = R7 - R2
  Addi(R9, R8, 2) # R9=R8+2
  Subi(R10, R9, 0x3) # 0x hex no.

Set(R11, 42)  # R11=42
Seth(R12, 0b1111) # 0b bin no.

  Store(R1, R11) # R1 is address to store data in R11
  Load(R6,R1) # R6 is data load from address R1

# conditional operation
Movez(R13, R2, R0) # R12=R2 if R0 = 0
Movex(R13, R3, R1) # R13=R3 if R1 != 0
Movep(R14, R3, R1) # R14=R3 if R1>=0
Moven(R10, PC, R3) # R10 = PC if R3<0

"""

# testing process
"""
print("...Loading asm program into memory...")
load(testprog)
printm()

print("...Runing test program...")
run()
printr()
printd()
"""