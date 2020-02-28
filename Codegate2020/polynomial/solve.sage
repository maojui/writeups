import numpy as np
from os import urandom
from IPython import embed
from sage.misc.banner import version_dict

class Chall:

    def __init__(self, N, p, q):
        self.N, self.p, self.q = N, p, q
        self.R = PolynomialRing(Integers(q), "x")
        self.x = self.R.gen()
        self.S = self.R.quotient(self.x ^ N - 1, "x")
        self.h, self.f = None, None

    def decrypt(self, e, privkey):
        e, privkey = self.S(e), self.S(privkey)
        temp = map(Integer, list(privkey * e))
        temp = [t - self.q if t > self.q // 2 else t for t in temp]
        temp = [t % self.p for t in temp]
        pt_encoded = [t - self.p if t > self.p // 2 else t for t in temp]
        pt = self.decode(pt_encoded)
        return pt

    def decode(self, value):
        out = sum([(value[i] + 1) * 3 ^ i for i in range(len(value))])
        return out

    def count(self, row):
        p = sum([e == 1 for e in row])
        n = sum([e == self.q - 1 for e in row])
        return p, len(row) - p - n, n


def solve(pubkey, cipher, counter, N, p, q, skip=[]) :
    chall = Chall(N,p,q)
    _h = [ h/Mod(p,q) for h in pubkey]
    h = [list(np.roll(_h,i)) for i in range(N) if i not in skip]
    H = Matrix(ZZ, matrix(h))
    C = Matrix(ZZ, cipher)
    I, O = identity_matrix, zero_matrix
    nr, nc = H.nrows(), H.ncols()
    a = (1/p)*I(nc)
    L = Matrix.block([
        [  a.delete_rows(skip)  ,      H       ],
        [  O(nc,nc)             ,   q * I(nc)  ],
    ])
    res = L.LLL()
    F = res[:,:N] * 3 # G = res[:,N:]
    mes = []
    for priv_key in map(list,F) :
        f = chall.S(priv_key)
        f = (f-1)/3
        if chall.count(list(f)) == counter :
            m = chall.decrypt(cipher, priv_key)
            mes.append(m)
    return mes

# get key1
N, p, q = (55, 3, 4027)
counter = (22, 18, 15)
pubkey = [3627, 1889, 3460, 2627, 3545, 1478, 2307, 3378, 3350, 1272, 2445, 3881, 3110, 1628, 1798, 1826, 259, 1983, 453, 52, 2650, 834, 3307, 907, 2762, 3452, 1085, 3059, 3544, 1136, 3767, 2346, 1952, 699, 3023, 531, 1208, 1449, 3636, 1742, 2692, 1128, 1683, 1152, 2584, 637, 3053, 2072, 2687, 1811, 2981, 3288, 2324, 3632, 1813]
cipher = [426, 3379, 3985, 160, 2502, 3592, 55, 1753, 3599, 2656, 2380, 582, 1038, 1028, 791, 1695, 1783, 3814, 3687, 3742, 1892, 1053, 2728, 3946, 801, 238, 3766, 1355, 1219, 528, 3560, 9, 3737, 1975, 1469, 85, 1373, 3717, 195, 3252, 2020, 1087, 201, 2536, 1655, 3380, 2322, 2438, 803, 2838, 1034, 457, 3050, 4010, 231]
key1 = solve(pubkey,cipher,counter,N,p,q)[0]
print(key1) 
# key1 = 12745833957649946853

# get key 2
N, p, q = (60, 3, 1499)
pubkey = [314, 1325, 1386, 176, 369, 1029, 877, 1255, 111, 1226, 117, 0, 210, 761, 938, 273, 525, 751, 1085, 372, 1333, 898, 780, 44, 649, 1463, 326, 354, 116, 1080, 1065, 1109, 358, 275, 1209, 964, 101, 950, 415, 1492, 1197, 921, 1000, 1028, 1400, 43, 1003, 914, 447, 360, 1171, 1109, 223, 1134, 1157, 1383, 784, 189, 870, 565]
cipher = [378, 753, 466, 825, 320, 658, 630, 288, 16, 576, 134, 914, 549, 489, 197, 1392, 328, 361, 1241, 50, 710, 315, 526, 1250, 977, 453, 225, 433, 1342, 1005, 1432, 143, 1326, 1426, 1251, 1397, 237, 1202, 555, 83, 994, 446, 1406, 356, 1127, 1469, 485, 1034, 1224, 230, 1445, 825, 630, 1158, 815, 807, 837, 747, 423, 184]
counter = (20, 20, 20)
for i in range(60) : 
    # i = [1,4,13,15,18,23,24,29,33,37,41,48,50,53,56,59]
    key2 = solve(pubkey,cipher,counter,N,p,q,skip=[i])
    if len(key1) : break
key2 = key2[0]
print(key2) 
# key2 = 5077410967206177007

from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

key1 = 12745833957649946853
key2 = 5077410967206177007
key = l2b(key1) + l2b(key2)
enc = 2960408776014513590203667205130185225161547470030516261741102417822093600856513664346223496713014612247754765985505434047965417819771431223015026059243409921418043319365743779292681722097463141
enc = l2b(enc)
cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(enc)
# flag = b'CODEGATE2020{86f94100f760b45e9c0f6925f5b474b24387ff6be5732ab88d74b4bfbff35951}\x02\x02'

