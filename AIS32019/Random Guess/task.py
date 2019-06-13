import os,random,sys,string
from Crypto.Util.number import getPrime,isPrime,GCD
import socketserver
import signal

class LCG:
    '''
    Linear Congruential Generator
    '''
    def __init__(self, seed, multiplier, increment, modulus):
        self.state = seed
        self.m = multiplier
        self.c = increment
        self.n = modulus

    def next(self,i=1):
        self.state = (self.state * self.m + self.c) % self.n
        return self.state


class Task(socketserver.BaseRequestHandler):

    def recv(self):
        return self.request.recv(1024).strip()

    def send(self, msg):
        if type(msg) == str :
            msg = bytes([ord(m) for m in msg])
        self.request.sendall(msg)
        
    def run(self,lcg):
        self.send('Random number a,b,c :\n')
        self.send('Given the set of number : Ni+1 = (a * Ni + b) % c :\nN = ')
        self.send(', '.join([str(lcg.next()) for _ in range(10)]))
        self.send('\nWhat is the next 100 number?\n')
        for _ in range(100):
            if int(self.recv()) != lcg.next() :
                self.send('Wrong!\n')
                raise Exception
            else :
                self.send('Good!\n')
        self.send('AIS3{GGEZ!!LiNe42_COngRuen7i4l_6eNErATor}\n')

    def handle(self):
        try :
            a = getPrime(25)
            b = getPrime(30)
            n = getPrime(30)
            n, b = max(b,n), min(b,n)
            seed = getPrime(30)
            lcg = LCG(seed,a,b,n)
            self.run(lcg)
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