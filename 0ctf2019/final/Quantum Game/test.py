
from pyquil import Program, get_qc

pp = Program('H 0 I 0')

qc = get_qc('1q-qvm')

result = qc.run_and_measure(pp, 10)[0]

print(result)