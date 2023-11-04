from Crypto.Util.number import *
from output import *

p1 = 21267647932558653966460912964485513283
a1 = 6701852062049119913950006634400761786
b1 = 19775891958934432784881327048059215186
p2 = 21267647932558653966460912964485513289
a2 = 10720524649888207044145162345477779939
b2 = 19322437691046737175347391539401674191
p3 = 21267647932558653966460912964485513327
a3 = 8837701396379888544152794707609074012
b3 = 10502852884703606118029748810384117800
a = [a1,a2,a3]
b = [b1,b2,b3]
p = [p1,p2,p3]
n = p1*p2*p3

r = []
for i in range(9):
    l = leaked[i*32:(i+1)*32]
    l = bytes_to_long(l)
    r.append(l)

mats = []
for i in range(3):
    mat = []
    m = Matrix.identity(GF(p[i]), 2)
    for j in range(9):
        mat.append(m)
        m *= Matrix(GF(p[i]), [[b[i],a[i]],[1,0]])
    mats.append(mat)

mat = []
for i in range(9):
    mati = [[0,0],[0,0]]
    for i1 in range(2):
        for i2 in range(2):
            if i1==0:
                c = CRT_list([int(mats[j][i][i1,i2])*(n//p[j])%p[j] for j in range(3)], p)
            else:
                c = CRT_list([int(mats[j][i][i1,i2]) for j in range(3)], p)
            mati[i1][i2] = c
    mat.append(mati)

for i in range(9):
    mat[i][0][0] = (mat[i][0][0]-r[i]*mat[i][1][0])%n
    mat[i][0][1] = (mat[i][0][1]-r[i]*mat[i][1][1])%n

M = [[0]*46 for _ in range(46)]
k = 0
for i in range(9):
    ai,bi,ci,di = mat[i][0][0],mat[i][0][1],mat[i][1][0],mat[i][1][1]
    for j in range(i):
        aj,bj,cj,dj = mat[j][0][0],mat[j][0][1],mat[j][1][0],mat[j][1][1]
        v1 = (ai*bj-aj*bi)%n
        v2 = (2**256)*(di*aj-ci*bj)%n
        v3 = (2**256)*(cj*bi-ai*dj)%n
        v4 = (2**512)*(ci*dj-cj*di)%n
        v1 = v1*inverse(v4,n)%n
        v2 = v2*inverse(v4,n)%n
        v3 = v3*inverse(v4,n)%n
        M[45][k] = -v1
        M[i][k] = -v2
        M[j][k] = -v3
        M[9+k][k] = n
        k += 1
weight = 2**100
for i in range(9):
    M[i][36+i] = weight
M[45][45] = 2**384

res = Matrix(M).LLL()

xs = [x//weight for x in res[-1][36:45]]
a0,b0,c0,d0 = mat[0][0][0],mat[0][0][1],mat[0][1][0],mat[0][1][1]
r = (-b0+(2**256)*xs[0]*d0)*inverse(int(a0-(2**256)*xs[0]*c0), n)%n
rs = [r%pi for pi in p]

def xor(a, b):
    return bytes([x^^y for x,y in zip(a, b)])

flag = b''
for i in range(2,-1,-1):
    for j in range(3):
        rs[j] = inverse(int(rs[j]-b[j]),p[j])*a[j]%p[j]
    ret = 0
    for j in range(3):
        ret += rs[j]*(n//p[j])
    ret %= n
    ret %= 2**256
    m = enc_flag[32*i:min(len(enc_flag),32*(i+1))]
    flag = xor(m,long_to_bytes(ret)) + flag
print(flag)
# b'SECCON{ICG1c6iC6icgic6icgcIgIcg1C6ic6ICGICG1cGicG1C61CG1cG1c61cgIcg}'
