import os,random,sys,string
from hashlib import sha256
import SocketServer

import des
from flag import FLAG

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.printable.strip()) for _ in xrange(20)])
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
            assert len(res)%8==0
        except:
            res = ''
        return res

    def dosend(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def genkey(self):
        tmp = os.urandom(8)
        key = ''
        for ch in tmp:
            key += chr(ord(ch)&0xfe)
        return key

    def handle(self):
        if not self.proof_of_work():
            return
        # We all know that DES can be bruteforced
        # But it should be longer then 20 minutes?
        self.request.settimeout(20*60)
        key = self.genkey()
        while True:
            self.dosend("plaintext(hex): ")
            pt = self.recvhex(20001)
            if pt=='':
                break
            ct = des.encrypt(pt, key)
            self.dosend("%s\n" % ct.encode('hex'))
        self.dosend("key(hex): ")
        guess = self.recvhex(20)
        if guess == key:
            self.dosend("nyao! %s\n" % FLAG)
        else:
            self.dosend("meow?\n")
        self.request.close()


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10001
    print HOST
    print PORT
    server = ThreadedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
