import os,random,sys,string
from hashlib import sha256
import SocketServer
import signal

FLAG = '1234123421421'

SZ = 8

def gbox(a,b,mode):
    x = (a+b+mode)%256
    return ((x<<2)|(x>>6))&0xff

def fbox(plain):
    t0 = (plain[2] ^ plain[3])
    y1 = gbox(plain[0] ^ plain[1], t0, 1)
    y0 = gbox(plain[0], y1, 0)
    y2 = gbox(t0, y1, 0)
    y3 = gbox(plain[3], y2, 1)
    return [y3, y2, y1, y0]

def doxor(l1,l2):
    return map(lambda x: x[0]^x[1], zip(l1,l2))

def encrypt_block(pt, ks):
    print(pt[:4],pt[4:])
    l = doxor(pt[:4], ks[4])
    r = doxor(doxor(pt[4:], ks[5]), l)
    print(l,r)
    print("Fbox :")
    for i in range(4):
        l, r = doxor(r, fbox(doxor(l,ks[i]))), l
        print(i, l ,r)

    l, r = r, doxor(l,r)
    print(l ,r)
    return l+r

def decrypt_block(ct,ks):
    l = ct[:4]
    r = ct[4:]
    print(l,r)
    l, r = doxor(l,r), l 

    print(l,r)
    print("Fbox :")
    for i in range(3,-1,-1):
        l, r = r, doxor(l, fbox(doxor(r,ks[i])))
        print(i, l ,r)
    
    print(l,r)
    r = doxor(doxor(r, l),ks[5])
    l = doxor(l, ks[4])
    print(l ,r)
    return l+r

def encrypt(pt, k):
    if SZ-len(pt) != 0 :
        x = SZ-len(pt)%SZ
        pt += chr(x)*x
    ct = ''
    print('start')
    for i in range(0, len(pt), SZ):
        res = encrypt_block(map(ord, pt[i:i+SZ]), k)
        ct += ''.join(map(chr,res))
    print('finish')
    return ct

def decrypt(pt, k):
    if SZ-len(pt) != 0 :
        x = SZ-len(pt)%SZ
        pt += chr(x)*x
    ct = ''
    print('start')
    for i in range(0, len(pt), SZ):
        res = decrypt_block(map(ord, pt[i:i+SZ]), k)
        ct += ''.join(map(chr,res))
    print('finish')
    return ct

def doout(x):
    tmp = ''.join(map(chr, x))
    return tmp.encode('hex')

def genkeys():
    subkeys=[]
    for x in xrange(6):
        subkeys.append(map(ord,os.urandom(4)))
    return subkeys

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def recvhex(self, sz):
        try:
            r = sz
            res = ''
            while r>0:
                res += self.request.recv(r)
                if res.endswith('\n'):
                    r = 0
                else:
                    r = sz - len(res)
            res = res.strip()
            res = res.decode('hex')
        except:
            res = ''
        return res

    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def handle(self):
        # if not self.proof_of_work():
        #     return
        # signal.alarm(30)
        key = genkeys()
        print key
        for i in xrange(50):
            self.dosend("plaintext(hex): ")
            pt = self.recvhex(81)
            print(pt)
            if pt=='':
                break
            ct = encrypt(pt, key)
            self.dosend("%s\n" % ct.encode('hex'))
        cflag = encrypt(FLAG, key)
        self.dosend("and your flag:\n")
        self.dosend("%s\n" % cflag.encode('hex'))
        self.request.close()


class ForkedServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    print HOST
    print PORT
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
