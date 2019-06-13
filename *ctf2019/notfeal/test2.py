import os


def gbox(a, b, mode):
    x = (a + b + mode) % 256
    return ((x << 2) | (x >> 6)) & 0xff


def fbox(plain):
    t0 = (plain[2] ^ plain[3])
    y1 = gbox(plain[0] ^ plain[1], t0, 1)
    y0 = gbox(plain[0], y1, 0)
    y2 = gbox(t0, y1, 0)
    y3 = gbox(plain[3], y2, 1)

    return [y3, y2, y1, y0]


def doxor(l1, l2):
    return [a ^ b for a, b in zip(l1, l2)]


def encrypt_block(pt, ks):
    dbg = []
    l, r = pt[:4], pt[4:]
    # dbg.append((l, r))

    l = doxor(l, ks[4])
    r = doxor(r, ks[5])
    # dbg.append((l, r))

    r = doxor(r, l)
    dbg.append((l, r))
    print(l,r)

    for i in range(4):
        l, r = doxor(r, fbox(doxor(l, ks[i]))), l
        print(i,l,r)
        dbg.append((l, r))

    l, r = r, doxor(l, r)
    dbg.append((l, r))
    return l + r, dbg


def genkeys():
    subkeys = []
    for x in range(6):
        subkeys.append(list(os.urandom(4)))
    return subkeys


def toint(arr):
    ret = 0
    for i, e in enumerate(arr):
        ret |= e << (8 * i)
    return ret


def hexx(i):
    return '0x' + hex(i)[2:].rjust(8, '0')


def printkey(ks):
    print('')
    for k in ks:
        print(hexx(toint(k)) + ',')


"""
def gen(ks, diff=0x80):
    for _ in range(5):
        pt1 = os.urandom(8)
        # pt2 = doxor(pt1, [0, 0, 0, 0, diff, diff, 0, 0])
        # pt2 = doxor(pt1, [diff, diff, 0, 0, 0, 0, 0, 0])
        # pt2 = doxor(pt1, [diff, diff, 0, 0, diff, diff, 0, 0])
        # pt2 = doxor(pt1, [0, 0, 0, 2, 0, 0, 0, 2])
        pt2 = doxor(pt1, doxor([0, 0, 0, 0, 0, 0, 0, 2], os.urandom(4) * 2))
        ct1, dbg1 = encrypt_block(pt1, ks)
        ct2, dbg2 = encrypt_block(pt2, ks)
        l1, r1 = toint(ct1[:4]), toint(ct1[4:])
        l2, r2 = toint(ct2[:4]), toint(ct2[4:])
        print('{ {%s, %s}, {%s, %s} },' % (hexx(l1), hexx(r1), hexx(l2), hexx(r2)))
        # print(dbg1[-3][1], dbg2[-3][1])
        # print(hexx(toint(doxor(dbg1[-5][1], dbg2[-5][1]))))
        
        # # print(hexx(toint(pt1[:4])), hexx(toint(pt1[4:])))
        # for l, r in dbg1:
        #     print(hexx(toint(l)), hexx(toint(r)))
        # print('')
        # # print(hexx(toint(pt2[:4])), hexx(toint(pt2[4:])))
        # for l, r in dbg2:
        #     print(hexx(toint(l)), hexx(toint(r)))
        # print('')
        # print('')
    print('')
"""


def genplain():
    ret = []
    for _ in range(5):
        pt1 = os.urandom(8)
        pt2 = doxor(pt1, [0, 0, 0, 0, 0x80, 0x80, 0, 0])
        ret.append((pt1, pt2))
    for _ in range(5):
        pt1 = os.urandom(8)
        pt2 = doxor(pt1, [0x80, 0x80, 0, 0, 0x80, 0x80, 0, 0])
        ret.append((pt1, pt2))
    for _ in range(5):
        pt1 = os.urandom(8)
        pt2 = doxor(pt1, [0, 0, 0, 2, 0, 0, 0, 2])
        ret.append((pt1, pt2))
    for _ in range(5):
        pt1 = os.urandom(8)
        pt2 = doxor(pt1, doxor([0, 0, 0, 0, 0, 0, 0, 2], os.urandom(4) * 2))
        ret.append((pt1, pt2))
    for _ in range(5):
        pt1 = os.urandom(8)
        pt2 = os.urandom(8)
        ret.append((pt1, pt2))
    return ret


def gencipher(ks, plain,idx):
    for pt1, pt2 in plain[idx:idx+5]:
        print('start')
        ct1, dbg1 = encrypt_block(pt1, ks)
        ct2, dbg2 = encrypt_block(pt2, ks)
        print('end')
        l1, r1 = toint(ct1[:4]), toint(ct1[4:])
        l2, r2 = toint(ct2[:4]), toint(ct2[4:])
        print('{ {%s, %s}, {%s, %s} },' % (hexx(l1), hexx(r1), hexx(l2), hexx(r2)))


def printplain(plain):
    for pt1, pt2 in plain:
        l1, r1 = toint(pt1[:4]), toint(pt1[4:])
        l2, r2 = toint(pt2[:4]), toint(pt2[4:])
        print('{ {%s, %s}, {%s, %s} },' % (hexx(l1), hexx(r1), hexx(l2), hexx(r2)))


