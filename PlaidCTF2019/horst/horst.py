import os
import random
from hashlib import sha1

M = 3
N = 64
n = 2

class Permutation:
    def __init__(self, L):
        self.n = len(L)
        self.L = L
        assert all(i in L for i in range(self.n))

    def __mul__(self, other):
        assert self.n == other.n
        return Permutation([other.L[self.L[i]] for i in range(self.n)])

    def __div__(self, other):
        assert self.n == other.n
        return Permutation([other.L[self.L[i]] for i in range(self.n)])

    def __eq__(self, other):
        return self.L == other.L

    def inv(self):
        return Permutation([self.L.index(i) for i in range(self.n)])

    def cycles(self):
        elts = list(range(self.n))
        cycles = []
        while len(elts) > 0:
            cur = []
            i = elts[0]
            while i not in cur:
                cur.append(i)
                elts.remove(i)
                i = self.L[i]
            cycles.append(cur)
        return cycles

    def __getitem__(self, i):
        return self.L[i]

    def __str__(self):
        return "".join("({})".format(" ".join(str(e) for e in c)) for c in self.cycles())

    def __repr__(self):
        return "Permutation({})".format(self.L)


def random_permutation(n):
    random.seed(os.urandom(100))
    L = list(range(n))
    for i in range(n-1):
        j = random.randint(i, n-1)
        L[i], L[j] = L[j], L[i]
    return Permutation(L)

for i in range(100):
    x = random_permutation(N)
    assert x * x.inv() == Permutation(list(range(N)))

def encrypt(m, k):
    x, y = m
    for i in range(M):
        x, y = (y, x * k.inv() * y * k)
    return x, y

def decrypt(c, k):
    x, y = c
    for i in range(M):
        x, y = (y * k.inv() * x.inv() * k, x)
    return x, y

if __name__ == "__main__":
    k = random_permutation(N)
    print "The flag is: PCTF{%s}" % sha1(str(k)).hexdigest()
    pairs = []
    for i in range(n):
        pt = random_permutation(N), random_permutation(N)
        ct = encrypt(pt, k)
        assert pt == decrypt(ct, k)
        pairs.append((pt,ct))

    with open("test.txt", "w") as f:
        f.write(str(pairs))
