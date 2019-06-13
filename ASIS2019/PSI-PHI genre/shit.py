import gmpy2
import os
import random
from Crypto.Util.number import isPrime

for i in range(10000):
    digit = random.randint(1,100)
    num = int(bytes.hex(os.urandom(digit)),16)
    nextPrime(num)
