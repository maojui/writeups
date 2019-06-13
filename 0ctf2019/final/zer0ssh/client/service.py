import os,random,sys,string
import subprocess
from hashlib import sha256
import SocketServer

class Task(SocketServer.BaseRequestHandler):
    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXX+%s) == %s\n" % (proof[3:],digest))
        self.request.send('Give me XXX:')
        x = self.request.recv(10)
        x = x.strip()
        if len(x) != 3 or sha256(x+proof[3:]).hexdigest() != digest: 
            return False
        self.request.sendall('OK\n')
        return True

    def handle(self):
        if not self.proof_of_work():
            return
        host = self.request.recv(20)
        host = filter(lambda x:x in '1234567890.', host)
        FNULL = open(os.devnull,"w")
        subprocess.call(["docker","run","--rm","zer0ssh",host],stdout=FNULL,stderr=FNULL)
        self.request.close()

class ForkedServer(SocketServer.ForkingTCPServer, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 3333
    print HOST
    print PORT
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
