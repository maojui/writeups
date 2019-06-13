from copy import copy, deepcopy
import random
from hashlib import sha256

class NotImplemented(Exception):
    pass

def xor(x,y):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(x,y))

def id_perm(N):
    return [i for i in range(N)]

def sort_perm(a, b, s, l, h):
    if l >= h:
        return

    u = id_perm(len(a))
    v = id_perm(len(a))
    w = id_perm(len(a))
    m = (l + h) / 2
    sort_perm(a, b, s, l, m)
    sort_perm(a, b, s, m + 1, h)

    u[m] = a[s[m]]
    v[m] = b[s[m]]
    if l < m:
        for i in reversed(range(l, m)):
            u[i] = min(a[s[i]], u[i+1])
            v[i] = min(b[s[i]], v[i+1])
    u[m+1] = a[s[m+1]]
    v[m+1] = b[s[m+1]]
    if h > m + 1:
        for i in range(m + 2, h+1):
            u[i] = max(a[s[i]], u[i - 1])
            v[i] = max(b[s[i]], v[i - 1])

    p = l
    q = m + 1
    for i in range(l, h+1):
        if p > m or (q <= h and u[p] > u[q] and v[p] > v[q]):
            w[i] = s[q]
            q += 1
        else:
            w[i] = s[p]
            p += 1
    for i in range(l, h+1):
        s[i] = w[i]

def rand():
    return random.randint(0, 2**32)

class Factor(object):
    def __init__(self, N, perm=None):
        self.N = N
        if perm is None:
            self.perm = id_perm(N)
        else:
            self.perm = perm

    @staticmethod
    def random(N):
        perm = id_perm(N)
        for i in range(N):
            j = i + rand() % (N - i)
            z = perm[i]
            perm[i] = perm[j]
            perm[j] = z
        return Factor(N, perm)

    @staticmethod
    def _delta_table(N, i, k):
        return N - i - 1 if (k & 1) else i

    @staticmethod
    def delta(N, k):
        D = Factor(N)
        for i in range(N):
            D.perm[i] = Factor._delta_table(N, i, k)
        return D

    def is_identity(self):
        return self.perm == id_perm(self.N)

    def right_multiply(self, b):
        for i in range(self.N):
            self.perm[i] = b.perm[self.perm[i]]

    def left_multiply(self, b):
        tmp = id_perm(self.N)
        for i in range(self.N):
            tmp[i] = self.perm[b.perm[i]]
        self.perm = tmp

    def flip(self, k):
        result = Factor(self.N)
        for i in range(self.N):
            d = Factor._delta_table
            result.perm[i] = d(self.N, self.perm[d(self.N, i, -k)], k)
        return result

    def left_meet(self, other):
        s = id_perm(self.N)
        a = copy(self.perm)
        b = copy(other.perm)
        sort_perm(a, b, s, 0, self.N-1)
        for i in range(self.N):
            self.perm[s[i]] = i

    def make_left_weighted(self, b):
        x = ~self * self.delta(1)
        x.left_meet(b)
        if x.is_identity():
            return False
        else:
            self.right_multiply(x)
            b.left_multiply(~x)
            return True

    def expand(self, N, offset):
        assert N >= self.N + offset
        newperm = id_perm(N)
        for i in range(self.N):
            newperm[i + offset] = self.perm[i] + offset
        self.perm = newperm
        self.N = N

    def invert(self):
        tmp = copy(self.perm)
        for i in range(self.N):
            tmp[self.perm[i]] = i
        self.perm = tmp

    def __mul__(self, other):
        if isinstance(other, Factor):
            result = deepcopy(self)
            result.right_multiply(other)
            return result
        elif isinstance(other, Braid):
            result = deepcopy(other)
            result.left_multiply(self)
            return result
        else:
            raise NotImplemented


    def __rmul__(self, other):
        result = deepcopy(self)
        result.left_multiply(other)
        return result

    def __invert__(self):
        result = deepcopy(self)
        result.invert()
        return result

    def __eq__(self, other):
        return self.perm == other.perm

    def __repr__(self):
        return repr(self.perm)

    __str__ = __repr__

class Braid(object):
    
    def __init__(self, N):
        self.N = N
        self.left_delta = 0
        self.right_delta = 0
        self.factors = []

    @staticmethod
    def random(N, length):
        res = Braid(N)
        for i in range(length):
            f = Factor.random(N)
            res *= f
        return res

    def left_multiply(self, other):
        if isinstance(other, Braid):
            self.left_delta += other.right_delta
            for f in reversed(other.factors):
                self.left_multiply(f)
            self.left_delta += other.left_delta
        elif isinstance(other, Factor):
            self.factors.insert(0, other.flip(self.left_delta))
        else:
            raise NotImplemented

    def right_multiply(self, other):
        if isinstance(other, Braid):
            self.right_delta += other.left_delta
            for f in other.factors:
                self.right_multiply(f)
            self.right_delta += other.right_delta
        elif isinstance(other, Factor):
            self.factors.append(other.flip(-self.right_delta))
        else:
            raise NotImplemented

    def to_normal_form(self):
        if self.right_delta != 0:
            self.factors = map(lambda f: f.flip(self.right_delta), self.factors)
            self.left_delta += self.right_delta
            self.right_delta = 0

        D = Factor.delta(self.N, 1)
        A = self.factors
        l = len(A) - 1
        for i in reversed(range(l+1)):
            for j in range(i, l):
                B = (~A[j]) * D
                B.left_meet(A[j+1])
                if B.is_identity():
                    break
                A[j].right_multiply(B)
                A[j+1].left_multiply(~B)

        while self.factors[0] == D:
            self.factors.pop(0)
            self.left_delta += 1

        while self.factors[-1].is_identity():
            self.factors.pop(-1)

    def expand(self, N, offset):
        assert N >= self.N + offset
        for f in self.factors:
            f.expand(N, offset)
        self.N = N

    def __eq__(self, other):
        if self.left_delta != other.left_delta:
            return False
        if self.right_delta != other.right_delta:
            return False
        if self.factors != other.factors:
            return False
        return True

    def __mul__(self, other):
        result = deepcopy(self)
        result.right_multiply(other)
        return result

    def __invert__(self):
        result = Braid(self.N)
        result.left_delta = -self.right_delta
        result.right_delta = 0
        f = Factor(self.N)
        for fp in reversed(self.factors):
            for i in range(self.N):
                f.perm[fp.perm[i]] = Factor._delta_table(self.N, i, 1)
            result.factors.append(f.flip(-result.right_delta))
            result.right_delta -= 1
        result.right_delta -= self.left_delta
        return result

    def __repr__(self):
        return repr((self.left_delta, self.factors, self.right_delta))

    __str__ = __repr__

if __name__ == "__main__":
    N = 140
    L = 20

    flag = open("flag").read().strip()
    assert len(flag) <= 32

    x = Braid.random(N, L)
    x.to_normal_form()

    a = Braid.random(N/2, L)
    a.expand(N, 0)

    y = a * x * (~a)
    y.to_normal_form()

    b = Braid.random(N/2, L)
    b.expand(N, N/2)

    c0 = b * x * (~b)
    c0.to_normal_form()

    c1 = b * y * (~b)
    c1.to_normal_form()

    enc = xor(sha256(str(c1)).digest(), flag).encode('hex')

    print (x,y)
    print (c0, enc)
