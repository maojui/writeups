import sys

def _l(idx, s):
    return s[idx:] + s[:idx]

s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
t = [[_l((i+j) % len(s), s) for j in range(len(s))] for i in range(len(s))]

def v3d(p, k):
    i = 0
    c = ""
    k2 = k[::-1]
    for a in p:
        c += t[s.find(a)][s.find(k[i])][s.find(k2[i])]
        i = (i + 1) % len(k)
    return c

def decrypt(c,k) :
    i = 0
    p = ""
    k2 = k[::-1]
    for a in c :
        for w in range(len(s)) :
            if a == t[w][s.find(k[i])][s.find(k2[i])] :
                p += s[w]    
        i = (i + 1) % len(k)
    return p

cand_khead = ''
cand_ktail = ''
known = 'SECCON{'

for i in range(len(known)) :
    cipher = 'POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9'
    for p in s :
        for q in s :
            k = ( cand_khead + p ).ljust(7,'?')
            k += ( q + cand_ktail ).rjust(7,'?')
            out = decode(cipher,k)
            if out[:i+1] == known[:i+1]:
                cand_khead += p 
                cand_ktail = q + cand_ktail
                print(out)
                print(p,q)
                break
        break
