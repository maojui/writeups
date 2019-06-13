import sys
from pwn import *
from cryptools import *
import string
import random
import itertools

def flip_bit(iv,i):
    # assert iv < 128, "OVER RANGE"
    iv = s2b(iv)
    flip = int(iv[i])^1
    iv = iv[:i] + str(flip) + iv[i+1:]
    return switchBS(b2s(iv)).rjust(16,b'\x00')


def count_bit(iv,i,len):
    # assert iv < 128, "OVER RANGE"
    len = len - (i+len-128+1) if (i+len) > 128  else len
    guess = 2**len
    iv = s2b(iv)
    ivs = []
    
    for g in range(guess) :
        temp = iv[:i+1] +s2b(n2s(g))[::-1][:len]
        if i+1+len > 128 :
            temp = temp[:128] 
        else :
            temp +=iv[i+1+len:]
        ivs.append(temp)
    return [switchBS(b2s(iv)).rjust(16,b'\x00') for iv in ivs ]


def payload(iv):
    return b64e(iv + any_num)

def state_change(payload,state):
    conn.recvuntil('guess : ')
    conn.sendline(payload)
    result = conn.recvuntil('\n')
    if b'small' in result :
        return state != 0
    elif b'big' in result :
        return state != 1
    else :
        print("FLAG : ", result)
        sys.exit(0)

def get_state(payload):
    conn.recvuntil('guess : ')
    conn.sendline(payload)
    result = conn.recvuntil('\n')
    print(result)
    if b'small' in result :
        return 0
    elif b'big' in result :
        return 1



pass_pow = False
while not(pass_pow):
    conn = remote('104.199.235.135', 20004)
    conn.recvuntil("x[:6] == '")
    start = conn.recvuntil("'").strip(b'\'')
    conn.recvuntil('\n')
    print(start)
    print(conn.recvuntil('x = '))
    i = 0
    count = 0 
    for c in itertools.product(string.digits + string.ascii_letters, repeat=6):
        count += 1
        tail_str = switchBS(''.join(c))
        if hashlib.sha256(start + tail_str).hexdigest().startswith('000000'):
            print("find")
            pass_pow = True
            conn.sendline(start + tail_str)
            break
        if count % 100000 == 0 : print(count)
        if count > 10000000:
            conn.close()
            break


print(conn.recvuntil('to number game ====='))

iv = b'\x00'*16
any_num = os.urandom(16)

s_change = 0
counter = 0
i = 0

while True:
    if i >= 128  :
        break

    flip_or_not = False
    state = get_state( payload(iv) )
    temp_iv = flip_bit(iv,i)
    
    state = state^1 if state_change(payload(temp_iv),state) else state 

    for test_iv in count_bit(temp_iv,i,7) :
        if state_change(payload(test_iv),state): # if one have change
            flip_or_not = True 
            break

    if flip_or_not :
        counter = 0
        iv = flip_bit(iv,i)
        s_change = i

    else :             # 超過 10 個沒動，機率有點低，可能翻錯：修正
        counter += 1
        if counter > 10 :
            i = s_change
            iv = flip_bit(iv,i)
            counter = 0

    print(i, s2b(iv))
    i+= 1
