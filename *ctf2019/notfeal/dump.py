from test import genplain, printplain, toint, hexx
from firstblood.all import uio
import string


r = uio.tcp('34.92.185.118', 10001)


suffix = r.after('XXXX+').until(')')
target = r.after('= ').line().strip().hexd

print('POW')
print(suffix)
print(target)

for p in (string.ascii_letters + string.digits).product(4):
    digest = (p + suffix).sha256
    if digest == target:
        print(p)
        break

r.line(p)

print('pts:')
plain = genplain()
printplain(plain)
print('')

print('cts:')
for pt1, pt2 in plain:
    pt1 = bytes(pt1)
    pt2 = bytes(pt2)
    r.line(pt1.hexe)
    ct1 = r.after('plaintext(hex): ').line().strip()[:16].hexd
    r.line(pt2.hexe)
    ct2 = r.after('plaintext(hex): ').line().strip()[:16].hexd
    # print(ct1)
    # print(ct2)
    l1, r1 = toint(ct1[:4]), toint(ct1[4:])
    l2, r2 = toint(ct2[:4]), toint(ct2[4:])
    print('{ {%s, %s}, {%s, %s} },' % (hexx(l1), hexx(r1), hexx(l2), hexx(r2)))

flag = r.after('and your flag:').nextline().line().strip().hexd.chunk(8).list
for f in flag:
    l1, r1 = toint(f[:4]), toint(f[4:])
    l2, r2 = toint(f[:4]), toint(f[4:])
    print('{ {%s, %s}, {%s, %s} },' % (hexx(l1), hexx(r1), hexx(l2), hexx(r2)))
    
print('flagSZ =', len(flag))

