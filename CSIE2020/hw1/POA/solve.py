from pwn import *

conn = remote('140.112.31.97', 30000)

conn.recvuntil('cipher =')
blocksize = 16
cipher = bytes.fromhex(conn.recvline().strip().decode())

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def oracle(c):
    conn.sendlineafter('cipher = ', c.hex())
    if conn.recvline().strip() == b'YESSSSSSSS':
        return True
    else:
        return False

flag = b''
for i in range(16, len(cipher), blocksize):
    ans = b''
    iv, block = cipher[i-16:i], cipher[i:i+16]
    for j in range(16):
        for k in range(256):
            if j == 15:
                if oracle(iv[:16 - 1 - j] + bytes([k]) + xor(iv[-j:], ans) + block):
                    ans = bytes([k ^ 0x80 ^ iv[16 - 1 - j]]) + ans
                    print(ans)
                    break
            else:
                if oracle(iv[:16 - 2 - j] + bytes([iv[16 - 2 - j] ^ 1]) + bytes([k]) + xor(iv[-j:], ans) + block):
                    ans = bytes([k ^ 0x80 ^ iv[16 - 1 - j]]) + ans
                    print(ans)
                    break
    flag += ans

conn.close()
print(flag)