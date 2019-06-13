from secret import FLAG
import os,random,sys,string
from Crypto.Util.number import getPrime,isPrime,GCD
import socketserver
import signal

class Task(socketserver.BaseRequestHandler):

    def recv(self):
        return self.request.recv(3000).strip()

    def send(self, msg):
        if type(msg) == str :
            msg = bytes([ord(m) for m in msg])
        self.request.sendall(msg)
        
    def run(self,phi):
        while True :
            self.send('n = ? \n')
            num = int(self.recv())
            self.send(f'(n % phi) % 64 = { str( ( num % phi ) % 64) }\n')
        
    def handle(self):
        try :
            while True :
                p = getPrime(1024)
                q = getPrime(1024)
                phi = (p-1)*(q-1)
                if GCD(phi,64) < 64 :
                    break
            n = p*q
            e = getPrime(random.randint(10,25))
            c = pow(FLAG,e,n)
            self.send(f'Public-key (e,N) : ({e},{n})\n')
            self.send('Encrypted Flag : ' + str(c))
            
            self.send('\n\nPHI Oracle : \n')
            print(phi)
            self.run(phi)
        except Exception as e:
            print(type(e), str(e))
            self.request.close()

class ForkingServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10201
    print(HOST,PORT)
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()