#!/usr/bin/env python3
# coding=utf-8

import pickle
import numpy as np
from math import pi, sqrt, asin
from pyquil import Program, get_qc
from pyquil.gates import *
from secret import flag

size = 4
num = 3200000

def encode(qid, msg):
    assert 0 <= msg < 16
    return RY(asin(sqrt(msg/16))*2, qid)

if __name__ == '__main__':
    assert len(flag) == size * 2
    print(f"Your flag is flag{{{flag}}}")
    msg = [int(i, 16) for i in flag]

    init = Program()
    for i, m in enumerate(msg):
        init += encode(i, m)
    qc = get_qc('16q-qvm')
    
    with open('program1', 'rb') as f:
        main = pickle.load(f)
    program = init + main
    reg = program.declare('ro', 'BIT', size)
    for i in range(size):
        program += MEASURE(i, reg[i])
    program.wrap_in_numshots_loop(num)
    result1 = qc.run(qc.compile(program))

    with open('program2', 'rb') as f:
        main = pickle.load(f)
    program = init + main
    reg = program.declare('ro', 'BIT', size)
    for i in range(size):
        program += MEASURE(size+i, reg[i])
    program.wrap_in_numshots_loop(num)
    result2 = qc.run(qc.compile(program))

    result = np.hstack((result1, result2))
    with open('result', 'wb') as f:
        pickle.dump(result, f)
