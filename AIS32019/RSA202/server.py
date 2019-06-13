import os
import socketserver
from Crypto.Util.number import getPrime, isPrime, inverse 

def next_prime(num):
    while True :
        num +=1
        if isPrime(num):
            return num

def s2n(s):
    """
    String to number.
    """
    if not len(s):
        return 0
    if type(s) == str :
        return int(''.join( hex(ord(c))[2:].rjust(2,'0') for c in s),16)
    if type(s) == bytes :
        return int.from_bytes(s,'big')

class Task(socketserver.BaseRequestHandler):

    def recv(self):
        return self.request.recv(1024).strip()

    def send(self, msg):
        if type(msg) == str :
            msg = bytes([ord(m) for m in msg])
        self.request.sendall(msg)

    def handle(self):
        try :
            self.send('Preparing your challenge ... \n')
            count = 0
            p,q,r = 0,0,0
            q = getPrime(1200)
            while True :
                count += 1
                print(count)
                r = getPrime(300)
                p = pow(r,4) + pow(r,3) + pow(r,2) + r + 1
                if isPrime(p) : 
                    print(r,p)
                    break
            self.send('Ok!\n')

            e = getPrime(30)
            self.send('e : ')
            self.send(str(e) + '\n')
            n1 = r * next_prime(r)
            self.send('n1 : r * next_prime(r)\n')
            self.send(str(n1) + '\n')
            n2 = p * q
            self.send('n2 : p * q\n')
            self.send(str(n2) + '\n')

            FLAG = 'AIS3{S0me7im3s_I_h4tE_factorDB}'
            FLAG1 = s2n(FLAG[:len(FLAG)//2])
            FLAG2 = s2n(FLAG[len(FLAG)//2:])

            enc1 = pow(FLAG1, e, n1)
            enc2 = pow(FLAG2, e, n2)

            self.send('enc : pow(FLAG1, e, n1)\n')
            self.send(str(enc1) + '\n')
            self.send('enc : pow(FLAG2, e, n2)\n')
            self.send(str(enc2) + '\n')
            self.send('\n')
            self.send('p,q,r are prime numbers.\n')
            self.send('\n')
            self.send('((p-1) % r)**2 + ((r**5 - 1) % p)**2 == 0\n')
            self.send('\n')
            self.send('Good luck !!')
            self.request.close()
        except:
            self.request.close()

class ForkingServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 33335
    print(HOST,PORT)
    server = ForkingServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()