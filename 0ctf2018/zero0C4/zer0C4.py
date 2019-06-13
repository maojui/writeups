#!/usr/bin/env python
# coding=utf-8

import string
import random
from os import urandom
from hashlib import sha256
from sys import argv
from struct import unpack
from SocketServer import ThreadingTCPServer, BaseRequestHandler, socket
from flag import flag

N = 5
mask = (1 << N) - 1
klen = 16

def ksa(key):
    """Key-scheduling algorithm for 0ops Cipher 4"""
    global N
    s = range(1 << N)
    i = 0
    j = 0
    while 1:
        i = (i + 1) & mask
        j = (j + s[i] + key[i%len(key)]) & mask
        s[i], s[j] = s[j], s[i]
        if not i:
            break
    return s

def prga(s, n):
    """Pseudo-random generation algorithm for 0ops Cipher 4"""
    i = 0
    j = 0
    res = bytearray()
    for _ in range(n):
        i = (i + 1) & mask
        j = (j + s[i]) & mask
        s[i], s[j] = s[j], s[i]
        res.append(s[(s[i]+s[j])&mask])
    return res


class zer0C4Handler(BaseRequestHandler):

    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in xrange(20)])
        digest = sha256(proof).hexdigest()
        self.request.send("sha256(XXXX+%s) == %s\n" % (proof[4:],digest))
        self.request.send('Give me XXXX:')
        x = self.request.recv(4)
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            return False
        return True

    def setup(self):
        self.ori_key = [ord(i) & mask for i in urandom(klen)]
        self.key = self.ori_key[:]

    def handle(self):
        try:
            self.core_handle()
        except socket.error as e:
            print e

    def core_handle(self):
        if not self.proof_of_work():
	    return
        self.request.send("Welcome to 0C4 Blackbox Server! Can you guess the key? (We are too lazy, so we provide you xor-key. Please encrypt your message with it by yourself:P)\n")
        for _ in xrange(1500):
            self.request.send("1. Generate new xor-key.\n2. Guess the key.\n")
            cmd = self.request.recv(2)
            if not cmd:
                break
            if cmd[0] == '1':
                self.request.send("Feel free to send some bytes:)\n")
                size = unpack('H', self.request.recv(2))[0]
                if size > 8192 or size % klen != 0:
                    self.request.send("Invalid size!\n")
                    break

                deltas = bytearray()
                while size:
                    recv_bytes = self.request.recv(size)
                    deltas += recv_bytes
                    size -= len(recv_bytes)
                deltas = [i & mask for i in deltas]

                xor_key = bytearray()
                key = self.key[:]
                for i in xrange(0, len(deltas), klen):
                    delta = deltas[i:i+klen]
                    key = [ii^jj for ii,jj in zip(key, delta)]
                    sbox = ksa(key)
                    xor_key += prga(sbox, 16)
                self.key = key
                self.request.send("Here is you xor-key: ")
                self.request.send(xor_key)

            elif cmd[0] == '2':
                self.request.send("Input the original key: ")
                guess_key = self.request.recv(klen)
                if map(ord, guess_key) == self.ori_key:
                    self.request.send("Here is what you what: {}\n".format(flag))
                else:
                    self.request.send("Wrong! You won't get anything:(\n")
                break
            else:
                self.request.send("Invalid command!\n")
        self.request.send("Bye!\n")

if __name__ == '__main__':
    ThreadingTCPServer.allow_reuse_address = True
    if len(argv) < 3:
        print "Usage: {} <IP> <PORT>".format(argv[0])
    else:
        ip = argv[1]
        port = int(argv[2])
        s = ThreadingTCPServer((ip, port), zer0C4Handler)
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print "shut down!"
            s.shutdown()
            s.socket.close()
