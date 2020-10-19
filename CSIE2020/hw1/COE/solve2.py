import z3
from functools import reduce

class z3lfsr():

    def __init__(self, state, feedback):
        self.state = state
        self.feedback = feedback

    def getbit(self):
        nextdata = (self.state << 1) 
        idx = self.state & self.feedback
        output = 0
        for shift in range(self.feedback.bit_length()):
            output ^= z3.LShR(idx, shift) & 1
        self.state = nextdata ^ output
        return output

keystream = [int(x) for x in open('output.txt','r').read()]

inits = [z3.BitVec(f'init{i}', 16) for i in range(3)]

l1 = z3lfsr(inits[0],39989)
l2 = z3lfsr(inits[1],40111)
l3 = z3lfsr(inits[2],52453)

def combine(x1,x2,x3):
    return (x1 & x2) ^ ((~x1) & x3)

solver = z3.Solver()

for i,b in enumerate(keystream[:100]):
    solver.add(b == combine(l1.getbit(),l2.getbit(),l3.getbit()))

print(solver.check())
m = solver.model()
print(m) # [init3 = 26730, init2 = 30057, init1 = 25702]

FLAG = ''
m = [25702, 30057, 26730]
for b in m :
    FLAG += ''.join([chr(bb) for bb in bytes.fromhex(hex(b)[2:])])
FLAG = f"FLAG{{{FLAG}}}"
#  FLAG{dfuihj}