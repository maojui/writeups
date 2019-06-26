import pickle
import numpy  as np
from sympy import *
from sys import exit

DEBUG = False
var('q:8')

with open('program1', 'rb') as f:
        program1 = pickle.load(f)
# with open('Quantum Measure/program2', 'rb') as f:
#         program2 = pickle.load(f)
# with open('Quantum Measure/result', 'rb') as f:
#         cha = pickle.load(f)
# with open('result', 'rb') as f:
#         cha = pickle.load(f)

prob = np.array([])

for k in range(16):
    res = {}
    qreg = []
    for i in range(16):
        a,b,c,d = bin(i)[2:].rjust(4,'0')
        a = q0 if int(a) else 16 - q0        
        b = q1 if int(b) else 16 - q1
        c = q2 if int(c) else 16 - q2
        d = q3 if int(d) else 16 - q3
        qreg.append(a*b*c*d)
    qreg = np.array(qreg)


    r4,r5,r6,r7 = [(k // (2**j)) % 2 for j in range (4)]
    e = q4 if int(r4) else 16 - q4        
    f = q5 if int(r5) else 16 - q5
    g = q6 if int(r6) else 16 - q6
    h = q7 if int(r7) else 16 - q7
    # Preprocess program
    process = ''
    goto = ''
    instructions = program1.instructions
    for instr in instructions :
        command, *param = str(instr).split(' ')
        if command == 'JUMP-WHEN':
            _to, reg = param
            reg = reg[reg.index('[')+1:-1]
            if int(locals()[f'r{reg}']) :
                goto = _to
        elif command == 'JUMP':
            if not goto :
                goto = param[0]
        elif command == 'LABEL':
            if goto == param[0] :
                goto = ''
        elif command == 'X':
            if goto == '':
                reg = int(param[0])
                if reg in range(4,8) :
                    locals()[f'r{reg}'] = 1 ^ int(locals()[f'r{reg}'])
                else :
                    process += f'{instr}\n'
            continue
        elif command in ['CNOT','SWAP']:
            if goto == '':
                process += f'{instr}\n'
            continue
        elif command in ['I','MEASURE','DECLARE']:
            pass
        else :
            raise ValueError("Value parse error.")
    process = process.strip().split('\n')


    
    for i in range(16):
        _in = bin(i)[2:].rjust(4,'0')
        _out = [int(i) for i in _in]
        for instr in process :
            command, *params = instr.split(' ')
            if command == 'SWAP' :
                a,b = [int(p) for p in params]
                _out[a], _out[b] = _out[b], _out[a]
            elif command == 'CNOT' :
                a,b = [int(p) for p in params]
                if _out[a] == 1 :
                    _out[b] = 1 ^ _out[b]
            elif command == 'X':
                idx = int(params[0])
                _out[idx] = 1 ^ _out[idx]
            else :
                raise ValueError("Error command QwQ...")
        # print(_in, int(''.join([str(o) for o in _out]),2))
        res[int(_in,2)] = int(''.join([str(o) for o in _out]),2)
    
    print(bin(res[0]))
    tmp = []
    for i in range(16) :
        idx = list(res.keys())[list(res.values()).index(i)]
        tmp.append(qreg[idx])

    tmp = np.array(tmp)

    tmp *= (e*f*g*h)
    
    if prob.size == 0 :
        prob = tmp.copy()
    else :
        prob += tmp.copy()



if not DEBUG :
    exit()

cc = [0]*16 
for c in cha: 
    tmp = int(''.join(map(str,c[:4])),2)    
    cc[tmp]+=1  
cprob = np.array(cc)/len(cha)

flag = '12340000'
q0,q1,q2,q3,q4,q5,q6,q7 = ['']

exec(f't = np.array({list(prob)})/(16**8)') 
for i,v in enumerate(cprob) : 
    quant = cprob[i]*100
    result = t[i]*100
    diff = abs(quant - result)
    print(f'{i:02d}',
        bin(i)[2:].rjust(4,'0'),
        f'{quant:05.2f}',
        f'{result:05.2f}',
        f'{diff:04.2f}'
        )

cbits = cprob * (16**8)
final = pow(prob[0] - int(cbits[0]),2)
for i in range(16): 
    print(f'long d{i} = pow({simplify(prob[i])}-{int(cbits[i])},2);') 
