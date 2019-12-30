import requests
import numpy as np
import random

sess = requests.Session()

basis = ['+'] * 512
z = [{'real': 1, 'imag': 0}, {'real': 0, 'imag': 1}]
state = [random.randrange(2) for _ in range(512)]
qubits = [z[s] for s in state]

res = sess.post('https://cryptoqkd.web.ctfcompetition.com/qkd/qubits', json={
    'basis': basis,
    'qubits': qubits,
}).json()

print(res)
bits = [s for s, b in zip(state, res['basis']) if b == '+'][:128]

key = int(''.join(map(str, bits)), 2).to_bytes(16, 'big')
shared = bytes.fromhex(res['announcement'])

key2 = bytes(a ^ b for a, b in zip(key, shared)).hex()
print(key2)