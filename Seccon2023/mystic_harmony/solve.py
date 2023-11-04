from Crypto.Util.number import *
import Crypto.Cipher.AES as AES
import hashlib

human_world_size = 64
spirit_world_size_param = 32
disharmony_count = 16

witch_map= [[79, 234, 66, 99, 151, 3, 58, 164, 80, 54, 3, 252, 174, 48, 173, 241, 24, 217, 80, 46, 135, 23, 136, 118, 62, 151, 13, 13, 201, 95, 120, 212], ... ]
treasure_box= b'\x99{d\xfe\x06\xc9\x07\x7f\xca\xc8\x01\xff\x857l\x10\x170\x99\xeb\xc0\xc9\xb4Q\x8a0\xe18\xd3F\x95\x99\xba\x99Y\x81R\xc5\\\xfa\x0c\xb5\x10CI\x18\xe0\x96\xd9k\x1d\x884{\xd9\x01(\xac\xc0)\xd2\x1a81'

R.<x> = PolynomialRing(GF(2))
size = 2^8
K.<alpha> = GF(size, modulus=x^8+x^4+x^3+x^2+1)

def inv(a, mod):
    b, x, y=mod, 1, 0
    while b:
        t=a//b
        a-=t*b
        x-=t*y
        a, b=b, a
        x, y=y, x
    return x%mod

def crt(r1, q1, r2, q2):
    g = inv(q2, q1)
    k = g*q2%q1
    g *= K(k)^(-1)
    return (g*(r1-r2)%q1)*q2+r2

G = prod(x-alpha^i for i in range(1,spirit_world_size_param+1))

# xの次数を求める
rs = []
for j in range(spirit_world_size_param):
    r = 0
    q = 1
    for i in range(spirit_world_size_param):
        v = 0
        if witch_map[j][i] is not None:
            v = alpha^witch_map[j][i]
        r = crt(v, x-alpha^(i+1), r, q)
        q *= (x-alpha^(i+1))
    r = r.list()
    r += [0]*(spirit_world_size_param-len(r))
    rs.append(r)

rst = Matrix(K, rs).transpose()
indx = []
for i in range(spirit_world_size_param+human_world_size):
    v = (x^i%G).list()
    v += [0]*(spirit_world_size_param-len(v))
    try:
        w = rst.solve_right(vector(K, v))
    except:
        continue
    indx.append(i)

# yの次数を求める
rs = []
for j in range(spirit_world_size_param):
    r = 0
    q = 1
    for i in range(spirit_world_size_param):
        v = 0
        if witch_map[i][j] is not None:
            v = alpha^witch_map[i][j]
        r = crt(v, x-alpha^(i+1), r, q)
        q *= (x-alpha^(i+1))
    r = r.list()
    r += [0]*(spirit_world_size_param-len(r))
    rs.append(r)

rst = Matrix(K, rs).transpose()
indy = []
for i in range(spirit_world_size_param+human_world_size):
    v = (x^i%G).list()
    v += [0]*(spirit_world_size_param-len(v))
    try:
        w = rst.solve_right(vector(K, v))
    except:
        continue
    indy.append(i)

# 係数を求める
M = [[K(0)]*(disharmony_count*disharmony_count) for _ in range(spirit_world_size_param*spirit_world_size_param)]
for i in range(spirit_world_size_param):
    for j in range(spirit_world_size_param):
        for k in range(disharmony_count):
            for l in range(disharmony_count):
                M[i*spirit_world_size_param+j][k*disharmony_count+l] = alpha^((i+1)*indx[k]+(j+1)*indy[l])

v = [K(0)]*(spirit_world_size_param*spirit_world_size_param)
for i in range(spirit_world_size_param):
    for j in range(spirit_world_size_param):
        if witch_map[j][i] is not None:
            v[i*spirit_world_size_param+j] = alpha^witch_map[j][i]

c = Matrix(K, M).solve_right(vector(K, v))

R.<x, y> = PolynomialRing(GF(2))
D = 0
for i in range(disharmony_count):
    for j in range(disharmony_count):
        D += c[i*disharmony_count+j]*x^indx[i]*y^indy[j]

def make_key(D):
    key_seed = b""
    for pos, value in sorted(list(D.dict().items())):
        x = pos[0]
        y = pos[1]
        power = discrete_log(value, alpha, size-1)
        key_seed += long_to_bytes(x) + long_to_bytes(y) + long_to_bytes(power)
    m = hashlib.sha256()
    m.update(key_seed)
    return m.digest()

key = make_key(D)
cipher = AES.new( key, AES.MODE_ECB )
print(cipher.decrypt(treasure_box))
# b'SECCON{I_te4ch_y0u_secret_spell...---number_XIV---Temperance!!!}'
