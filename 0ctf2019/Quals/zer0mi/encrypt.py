# Failed attempt with sage, so write my own
# Sorry for the slow implementation. If you want to test with smaller N you should change Polynomial.Q as well. 
# Using pypy and a small th would also be helpful.
from os import urandom
from random import randrange
from fractions import gcd
from copy import copy, deepcopy

class NotImplemented(Exception):
    pass

B = 8
class GF256(object):
    def __init__(self, n=0):
        assert n>=0 and n<256
        self.v = []
        for _ in range(B):
            self.v.append(n%2)
            n/=2

    def int(self):
        res = 0
        for i in reversed(self.v):
            res = res*2+i
        return res

    def __add__(self, x):
        if isinstance(x, GF256):
            res = deepcopy(self)
            for i in range(B):
                res.v[i] ^= x.v[i]
            return res
        else:
            raise NotImplemented
        
    def __mul__(self, x):    
        def mul2x(v, i):
            v = [0]*i + v
            for i in reversed(range(B, len(v))):
                if v[i]!=0:
                    v[i]^=1
                    v[i-4]^=1
                    v[i-5]^=1
                    v[i-6]^=1
                    v[i-8]^=1
            return v[:B]

        if isinstance(x, GF256):
            res = GF256()
            for i in range(B):
                if self.v[i]==0:
                    continue
                tmp = mul2x(x.v, i)
                for j in range(B):
                    res.v[j] ^= tmp[j]
            return res
        elif isinstance(x, Expression):
            return x*self
        else:
            raise NotImplemented

    def __repr__(self):
        res = map(lambda (a,_):"z8^%d"%a if a>1 else "z8" if a==1 else "1", filter(lambda (_,a):a!=0, enumerate(self.v)))
        if len(res)>0:
            return ' + '.join(reversed(res))
        else:
            return '0'

N = 63
class Expression(object):
    # For each term, we have at most two variables
    # So we represent a*xi^b*xj^c as (a,i,b,j,c) (i<j),
    # a*xi^b as (a,-1,-1,i,b),
    # and a as (a,-1,-1,-1,-1) 
    def __init__(self, v=[]):
        self.v = deepcopy(v)

    @staticmethod
    def cmp_term(t0, t1):
        if t0[1]<t1[1]:
            return 1
        elif t0[1]>t1[1]:
            return -1
        elif t0[3]<t1[3]:
            return 1
        elif t0[3]>t1[3]:
            return -1
        elif t0[2]<t1[2]:
            return 1
        elif t0[2]>t1[2]:
            return -1
        elif t0[4]<t1[4]:
            return 1
        elif t0[4]>t1[4]:
            return -1
        else:
            return 0

    @staticmethod
    def mult_term(t0, t1):
        if t0[1]!=-1 or t1[1]!=-1:
            raise NotImplemented
        if t0[3]<t1[3]:
            return (t0[0]*t1[0], t0[3], t0[4], t1[3], t1[4])
        elif t0[3]>t1[3]:
            return (t0[0]*t1[0], t1[3], t1[4], t0[3], t0[4])
        else:
            return (t0[0]*t1[0], -1, -1, t0[3], (t0[4]+t1[4])%255)

    @staticmethod
    def eliminate_term(ts):
        res = []
        v = [False]*len(ts)
        for i in range(len(ts)):
            if v[i]:
                continue
            coef = ts[i][0]
            for j in range(i+1,len(ts)):
                if ts[i][1]==ts[j][1] and ts[i][2]==ts[j][2] and ts[i][3]==ts[j][3] and ts[i][4]==ts[j][4]:
                    coef += ts[j][0]
                    v[j] = True
            if coef.int()!=0:
                res.append((coef,ts[i][1],ts[i][2],ts[i][3],ts[i][4]))
        return res

    @staticmethod
    def repr_term(t):
        coef = repr(t[0])
        if coef=='0':
            return coef
        term = '('+coef+')*'
        if t[1]!=-1:
            term += 'x%d^%d*' % (t[1], t[2]) if t[2]!=1 else 'x%d*' % t[1]
        if t[3]!=-1:
            term += 'x%d^%d' % (t[3], t[4]) if t[4]!=1 else 'x%d' % t[3]
        return term.strip('*')

    def square(self):
        res = []
        for i in range(len(self.v)):
            if self.v[i][1]!=-1:
                raise NotImplemented
            res.append((self.v[i][0]*self.v[i][0],-1,-1,self.v[i][3],(self.v[i][4]*2)%255))
        return Expression(res)

    def subs(self, x):
        assert len(x)==N
        res = GF256()
        for t in self.v:
            tmp = deepcopy(t[0])
            for _ in range(t[2]):
                tmp *= x[t[1]]
            for _ in range(t[4]):
                tmp *= x[t[3]]
            res += tmp
        return res

    def __add__(self, x):
        if isinstance(x, Expression):
            res = []
            i = 0
            j = 0
            while i<len(self.v) or j<len(x.v):
                if i>=len(self.v):
                    res.append(copy(x.v[j]))
                    j+=1
                    continue
                if j>=len(x.v):
                    res.append(copy(self.v[i]))
                    i+=1
                    continue
                order = self.cmp_term(self.v[i],x.v[j])
                if order==1:
                    res.append(copy(self.v[i]))
                    i+=1
                elif order==-1:
                    res.append(copy(x.v[j]))
                    j+=1
                else:
                    t0 = self.v[i]
                    t1 = x.v[j]
                    res.append((t0[0]+t1[0],t0[1],t0[2],t0[3],t0[4]))
                    i+=1
                    j+=1
            return Expression(res)
        else:
            raise NotImplemented

    def __mul__(self, x):    
        if isinstance(x, Expression):
            res = []
            for t0 in self.v:
                for t1 in x.v:
                    res.append(self.mult_term(t0, t1))
            res = self.eliminate_term(res)
            return Expression(res)
        elif isinstance(x, GF256):
            res = []
            for t0 in self.v:
                res.append((t0[0]*x,t0[1],t0[2],t0[3],t0[4]))
            return Expression(res)
        else:
            raise NotImplemented

    def __repr__(self):
        res = filter(lambda x:x!='0',map(self.repr_term, self.v))
        if len(res)>0:
            return ' + '.join(res)
        else:
            return '0'

class Polynomial(object):
    # quotient as x^63 + z8^5*x^62 + (z8^7 + z8)*x^61 + z8*x^60 + (z8^7 + z8^6 + z8^5 + z8^4 + z8)*x^59 + (z8^6 + z8^5 + z8^3 + z8 + 1)*x^58 + (z8^6 + z8^5 + z8^3 + z8 + 1)*x^57 + (z8^7 + z8^6 + z8^3)*x^56 + (z8^3 + z8 + 1)*x^55 + (z8^4 + z8)*x^54 + (z8^5 + z8^3)*x^53 + (z8^7 + z8^6 + z8^2 + z8)*x^52 + (z8^5 + 1)*x^51 + (z8^6 + z8^2 + z8)*x^50 + (z8^5 + z8 + 1)*x^49 + (z8^5 + z8^4 + z8^3 + 1)*x^48 + (z8^7 + z8^3 + z8^2 + z8 + 1)*x^47 + (z8^7 + z8^6 + z8^5 + z8^3 + 1)*x^46 + z8^4*x^45 + (z8^3 + 1)*x^44 + (z8^4 + z8^2 + z8)*x^43 + (z8^5 + 1)*x^42 + (z8^5 + z8^4 + z8)*x^41 + (z8^7 + z8^5 + z8^2)*x^40 + (z8^6 + z8^5 + z8^3 + z8 + 1)*x^39 + (z8^7 + z8^5 + z8^4 + z8^2)*x^38 + (z8^6 + z8^5 + z8^4 + z8^3 + z8^2)*x^37 + (z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2 + z8)*x^36 + (z8^6 + z8^3 + 1)*x^35 + z8^3*x^34 + (z8^4 + z8^3 + z8^2)*x^33 + (z8^7 + z8^5 + z8)*x^32 + (z8^7 + z8^6 + z8^4 + z8^3 + z8^2)*x^31 + (z8^6 + z8^5 + 1)*x^30 + (z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2 + z8 + 1)*x^29 + (z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2 + z8)*x^28 + (z8^6 + z8^5 + z8^4 + z8^3)*x^27 + (z8^7 + z8^5 + z8^4 + 1)*x^26 + (z8^7 + z8^6 + z8^5 + z8^4 + z8^2)*x^25 + (z8^5 + z8^2 + z8 + 1)*x^24 + z8^7*x^23 + (z8^7 + z8^6 + z8)*x^22 + (z8^7 + 1)*x^21 + (z8^6 + z8^4 + z8^2)*x^20 + (z8^5 + 1)*x^19 + (z8^2 + 1)*x^18 + (z8^7 + z8^5 + z8^4 + z8^2 + z8 + 1)*x^17 + (z8^7 + z8^6 + z8^5 + z8^4)*x^16 + (z8^7 + z8^5 + z8^4 + z8^2 + z8)*x^15 + (z8^7 + z8^3 + z8)*x^14 + (z8^7 + z8^4 + z8^3 + z8)*x^13 + (z8^3 + z8^2 + 1)*x^12 + (z8^7 + z8^5 + z8^2)*x^11 + (z8^7 + z8^3 + z8 + 1)*x^10 + (z8^7 + z8^5 + z8^3 + 1)*x^9 + (z8^5 + z8^4 + z8^2 + z8)*x^8 + (z8^7 + z8^5 + z8^4 + z8^2 + z8 + 1)*x^7 + (z8^6 + z8^2 + 1)*x^6 + z8^6*x^5 + (z8^7 + z8)*x^4 + (z8^7 + z8^5 + z8^2)*x^3 + (z8^7 + z8^4)*x^2 + (z8^7 + z8^5 + z8^3)*x + z8^7
    Q = map(lambda x:GF256(x), [128, 168, 144, 164, 130, 64, 69, 183, 54, 169, 139, 164, 13, 154, 138, 182, 240, 183, 5, 33, 84, 129, 194, 128, 39, 244, 177, 120, 254, 255, 97, 220, 162, 28, 8, 73, 254, 124, 180, 107, 164, 50, 33, 22, 9, 16, 233, 143, 57, 35, 70, 33, 198, 40, 18, 11, 200, 107, 107, 242, 2, 130, 32])
    def __init__(self, v):
        self.v = []
        for i in range(N):
            if i<len(v):
                assert isinstance(v[i], Expression)
                self.v.append(deepcopy(v[i]))
            else:
                self.v.append(Expression())

    @staticmethod
    def mod(v):
        for i in reversed(range(N, len(v))):
            for j in range(1, N+1):
                v[i-j] += v[i]*Polynomial.Q[N-j]
        return v[:N]

    def export(self):
        return deepcopy(self.v)

    def square(self):
        res = []
        for i in range(N):
            res.append(self.v[i].square())
            res.append(Expression())
        self.v = self.mod(res)
        
    def __add__(self, x):
        if isinstance(x, Polynomial):
            res = deepcopy(self)
            for i in range(N):
                res.v[i] += x.v[i]
            return res
        else:
            raise NotImplemented

    def __mul__(self, x):
        if isinstance(x, Polynomial):
            res = []
            for _ in range(2*N):
                res.append(Expression())
            for i in range(N):
                for j in range(N):
                    res[i+j] += self.v[i]*x.v[j]
            return Polynomial(self.mod(res))
        else:
            raise NotImplemented

    def __repr__(self):
        res = filter(lambda (_,x):x!='0',enumerate(map(repr, self.v)))
        res = map(lambda (a,b):"(%s)*x^%d"%(b,a) if a>1 else "(%s)*x"%b if a==1 else b, reversed(res))
        if len(res)>0:
            return ' + '.join(res)
        else:
            return '0'

def gen_affine():
    mat = []
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(GF256(randrange(0,256)))
        mat.append(row)
    # should check whether the matrix is inversible
    return mat

def mat_mult(mat, vec):
    assert len(mat)>0 and len(mat[0])==len(vec)
    res = []
    for i in range(len(mat)):
        tmp = Expression()
        for j in range(len(vec)):
            tmp += mat[i][j]*vec[j]
        res.append(tmp)
    return res

def main():
    with open('flag') as f:
        flag = f.read()
    a = map(lambda x:GF256(x), map(ord, flag)+map(ord, urandom(N-len(flag))))
    q = 2**B
    th = randrange(1,N)
    while gcd(q**th+1,q**N-1)!=1:
        th = randrange(1,N)
    l1 = gen_affine()
    l2 = gen_affine()
    v = [Expression([(GF256(1),-1,-1,i,1)]) for i in range(N)]
    v = mat_mult(l2, v)
    p1 = Polynomial(v)
    for i in range(B*th):
        p1.square()
    p = Polynomial(v)*p1
    pubkey = mat_mult(l1, p.export())
    print pubkey
    ct = map(lambda x:x.subs(a), pubkey)
    ct = ''.join(map(lambda x:chr(x.int()), ct))
    print ct.encode('hex')

if __name__ == '__main__':
    main()
