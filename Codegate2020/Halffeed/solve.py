from pwn import *

def pad(data):
    assert isinstance(data, bytes)
    assert len(data) <= 16

    if len(data) != 16:
        data += b'\x01' + b'\x00' * (15 - len(data))
    return data

def feed_plus(tag, data):
    assert isinstance(tag, bytes) and isinstance(data, bytes)
    assert len(tag) == 16 and len(data) <= 16

    enc_data = bytes(b1 ^ b2 for b1, b2 in zip(tag, data))
    feed_data = pad(data)[:8] + pad(enc_data)[8:]
    tag = bytes(b1 ^ b2 for b1, b2 in zip(tag, feed_data))

    return tag, enc_data

# HOST = '127.0.0.1'
# PORT = 10000
HOST = '110.10.147.44'
PORT = 7777

conn1 = remote(HOST,PORT)
conn1.recvuntil('>')

conn1.sendline('1')
conn1.recvuntil('plaintext =')

p = b'\x00'*32
conn1.sendline(p.hex())
c = bytes.fromhex(conn1.recvline().strip().decode().split(' = ')[1])
t = bytes(b1 ^ b2 for b1, b2 in zip(c, p))
t1 = t[16:]
conn1.close()

conn2 = remote(HOST,PORT)
conn2.recvuntil('>')
conn2.sendline('1')
conn2.recvuntil('plaintext =')

p1= b';cat fla'.rjust(16,b'\x00')
p2 = b'\x00'*16
p = p1 + p2

conn2.sendline(p.hex())
c = bytes.fromhex(conn2.recvline().strip().decode().split(' = ')[1])
c1 = c[:16]
c2 = bytes(b1 ^ b2 for b1, b2 in zip(c[16:], b'g;'.ljust(16,b'\x00')))
cipher = c1 + c2

t = bytes(b1 ^ b2 for b1, b2 in zip(c, p))
t2 = t[16:]
conn2.close()





conn3 = remote(HOST,PORT)
conn3.recvuntil('>')
conn3.sendline('1')
conn3.recvuntil('plaintext =')

t_out, c_ = feed_plus(t2, b'g;'.ljust(16,b'\x00'))
f1 = bytes(b1 ^ b2 for b1, b2 in zip(t1[:8], t_out[:8]))
f2 = t_out[8:]
f = b'\x00'*16 + f1 + f2

conn3.sendline(f.hex())
conn3.recvuntil('tag =')
tag = bytes.fromhex(conn3.recvline().strip().decode())
conn3.close()

# afcd6b3562eb393ac792b2ee19f6a734

conn4 = remote(HOST,PORT)
conn4.recvuntil('>')
conn4.sendline('3')

nonce = b'\x00' * 16
conn4.sendline(nonce.hex())
conn4.sendline(cipher.hex())
conn4.sendline(tag.hex())

conn4.interactive()

# CODEGATE2020{F33D1NG_0N1Y_H4LF_BL0CK_W1TH_BL0CK_C1PH3R}