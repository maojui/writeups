#!/usr/bin/env python3
# coding=utf-8

import socketserver
import signal
import os
import random
import string
from hashlib import sha256
from pyquil import Program, get_qc
# from secret import flag
flag = 'flag{D0_yoU_eNj0y_f4nta5tIc_QuaNtum_9aMe?}'

def rand_choice():
    if (os.urandom(1)[0] & 1):
        return Program('X 0')
    else:
        return Program('I 0')

class handler(socketserver.BaseRequestHandler):
    def send(self, msg):
        self.request.sendall(msg+b'\n')

    def recv(self, n):
        return self.request.recv(n)

    def exit(self, msg):
        self.send(msg)
        self.request.close()
        exit()

    def get_choice(self):
        try:
            choice = Program(self.recv(100).decode('ascii'))
            assert 'DE' not in str(choice)
            return choice
        except Exception as e:
            print(type(e), e)
            self.exit(b'What are you doing?!')

    def proof_of_work(self):
        proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
        proof = proof.encode('ascii')
        digest = sha256(proof).hexdigest()
        self.send(f"sha256(XXXX+{proof[4:].decode('ascii')}) == {digest}".encode('ascii'))
        self.send(b'Give me XXXX:')
        x = self.recv(4)
        if len(x) != 4 or sha256(x+proof[4:]).hexdigest() != digest: 
            self.exit(b'No no no :(')

    def stage1_2(self):
        self.send(b'Level 1 - flipping coin (defeat the enemy)')
        self.send(b'Your turn: ("I 0" for not flipping and "X 0" for flipping)')
        choice1 = self.get_choice()
        self.send(b'Your enemy\'s turn...')
        self.send(b'Your turn again: ("I 0" for not flipping and "X 0" for flipping)')
        choice2 = self.get_choice()
        # Luckiness won't save you :)
        result = []
        for i in range(100):
            stage1 = choice1 + rand_choice() + choice2
            one_result = self.qc.run_and_measure(stage1, 1)[0]
            result.append(one_result[0])
        if all(result):
            self.send(b'You win!')
        else:
            self.exit(b'You lose...')

        self.send(b'Level 2 - flipping coin (defeat yourself)')
        stage2 = Program()
        self.send(b'Your enemy\' s turn...')
        stage2 += choice1
        self.send(b'Your turn: ("I 0" for not flipping and "X 0" for flipping)')
        your_choice = self.get_choice()
        stage2 += your_choice
        self.send(b'Your enemy\' s turn again...')
        stage2 += choice2
        result = self.qc.run_and_measure(stage2, 100)[0]
        if any(result):
            self.exit(b'You lose...')
        else:
            self.send(b'You win!')

    def stage3(self):
        target = random.randint(1000, 99000)
        self.send(f'level3 - coin master (get {target} heads in 100000 tosses)'.encode('ascii'))
        self.send(b'How do you toss the coin? ("I 0" for tail and "X 0" for head)')
        try:
            toss = Program(self.recv(100).decode('ascii'))
            assert 'DE' not in str(toss)
            result = self.qc.run_and_measure(toss, 100000)[0]
            cnt = sum(result==1)
            diff = abs(target-cnt)
            print(diff)
            if diff < 100:
                self.send(b'You win!')
            else:
                self.exit(b'You lose...')
        except Exception as e:
            print(type(e), e)
            self.exit(b'What are you doing?!')

    def setup(self):
        random.seed(os.urandom(8))
        self.qc = get_qc('1q-qvm')

    def handle(self):
        signal.alarm(300)
        # self.proof_of_work()
        signal.alarm(300)
        self.send(b'===============================================================')
        self.send(b'Welcome to Quantum Coin Game! Win all games and get your flag! ')
        self.send(b'===============================================================')

        self.stage1_2()
        self.stage3()
        self.send(f'Congratulations! Here is what you want: {flag}'.encode('ascii'))

        self.request.close()

class ForkingServer(socketserver.ForkingTCPServer, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 13337
    ForkingServer.allow_reuse_address = True
    server = ForkingServer((HOST, PORT), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutdown!')
        server.shutdown()
