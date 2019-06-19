
import pickle
import numpy as np
from math import pi, sqrt, asin
from pyquil import Program, get_qc
from pyquil.gates import *

size = 2
num = 1000

program = Program()
qc = get_qc('16q-qvm')
reg = program.declare('ro', 'BIT', size)

program += H(0)
program += MEASURE(0,reg[0])
program.if_then(reg[0],H(1),X(1))

for i in range(size):
    program += MEASURE(i, reg[i])

program.wrap_in_numshots_loop(num)
result = qc.run(qc.compile(program))
print(result)