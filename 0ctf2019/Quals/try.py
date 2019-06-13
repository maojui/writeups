from pwn import *
conn = remote('127.0.0.1',10002)

def test(plaintext):
    conn.recvuntil('plaintext(hex): ')
    plaintext = plaintext
    conn.sendline(plaintext)
    return conn.recvuntil('\n').strip()

print(test('00' * 8))
print(test('00' * 7 + '01'))
