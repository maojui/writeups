from pwn import *

target = list(set(b'\x00getmd5 31337313373133731337313373133731ca61e7186846286e8b7b45364b4efcd9\x00'))
querylist = list(set(target))
querylist += [x for x in range(256) if x not in querylist]

def byte(x):
    s = io.BytesIO()
    s.write( bytearray( (x,) ) )
    return s.getvalue()

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

def n2s(n,byteorder='big'):
    """
    Number to string.
    """
    length = (len(hex(n))-1)//2
    return int(n).to_bytes(length=length,byteorder=byteorder)

def xor_string(s1,s2):
    """
    Exclusive OR (XOR) @s1, @s2 byte by byte
    return the xor result with minimun length of s1,s2
    """
    if type(s1) != type(s2) :
        raise TypeError('Input must be the same type, both str or bytes.')
    if type(s1) == type(s2) == bytes :
        return b''.join([byte(a^b) for a,b in zip(s1,s2)])
    return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)])

def xor(string, index, ascii) :
    if index < 0 :
        index = index % len(string)
    return string[:index] + bytes([string[index] ^ ascii]) + string[index+1:]

def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

while True :
    print("----------  Start -----------")
    count = 0
    conn = remote('eof-exam2.ais3.org', 31337)
    # conn = remote('localhost', 13001)
    conn.recvuntil(': ') # Team token
    teamToken = 'zFErzItq'
    conn.sendline(teamToken)
    try:
        while True :
            print(conn.recvuntil('\n'))
            cipher = conn.recvuntil('\n')[:-1]
            print(cipher)
            cipher = n2s(int(cipher,16))
            print(cipher)
            blocks = chunk(cipher,16)
            subarray = [False, False]
            subword = [None, None]

            for i in range(2,len(blocks)):
                flag = False
                word = None

                for c in target : 
                    payload = b''.join(blocks[:i]) + xor(xor(blocks[i],15,c),15,1)
                    payload = hex(s2n(payload))[2:]
                    if len(payload) %2 != 0 :
                        payload = '0' + payload
                    conn.recvuntil(': ')
                    conn.sendline(payload)
                    result = conn.recvuntil('\n')
                    if b"padding" not in result :
                        # print(chr(c))
                        if b'MD5' in result :
                            continue
                        word = chr(c)
                        flag = True
                        break
                subword.append(word)
                subarray.append(flag)

            print(subarray)
            trueLine = {}
            for i in range(len(subarray)-1) :
                if subarray[i] == True :
                    trueLine[i] = sum(subarray[i:i+5])
                else :
                    trueLine[i] = 0
            blockIDX = max(trueLine.items(), key=operator.itemgetter(1))[0]

            while True :
                if not subword[blockIDX].isdigit() :
                    if subword[blockIDX] in '\x00getmd5 ':
                        break
                    blockIDX += 1
                else :
                    break

            # result = tmpC[blockIDX+5]
            # print(subarray)
            def paddingOracle(blocks, blockIDX) :
                global count
                cblock = blocks[blockIDX]
                pblock = b''
                for pad in range(1,17):
                    payload = cblock
                    payload = xor_string(payload,pblock.rjust(16,b'\x00'))
                    payload = xor_string(payload,( bytes([pad]) * (pad-1) ).rjust(16,b'\x00'))
                    find = False

                    for idx in querylist : 
                        if idx == b'\x00':
                            continue
                        count += 1
                        tp = xor(payload,16-pad,idx)
                        tmp = b''.join(blocks[:blockIDX]) + tp
                        tmp = hex(s2n(tmp))[2:]
                        if len(tmp) %2 != 0 :
                            tmp = '0' + tmp

                        conn.recvuntil(': ')
                        conn.sendline(tmp)


                        result = conn.recvuntil('\n')

                        if b"padding" not in result :
                            if b'MD5' in result :
                                if pad == 1 and len(blocks) == blockIDX -1 :
                                    continue
                            pblock = bytes([idx ^ pad]) + pblock
                            find = True
                            break
                    if not find :
                        print("FAIL BLOCK")
                        raise Exception("FUCK YOU")
                        print(cblock)
                        print(pblock.rjust(16,b'\x00'))
                        print(( bytes([pad]) * (pad-1) ).rjust(16,b'\x00'))
                        print()
                print(count)
                return pblock.rjust(16,b'\x00') 
            
            wholeplain = b''
            offset = 2
            incr = 1
            crc32IDX = 1e9
            crc32_seg = ''
            while True : 
                if len(blocks) -1 >= blockIDX+offset + incr :
                    wholeplain += paddingOracle(blocks,blockIDX+offset + incr)
                    print(wholeplain)
                else :
                    break
                if b'\x00' in wholeplain :
                    break
                incr += 1
            print(wholeplain)

            something_Dirty = True
            while something_Dirty :
                something_Dirty = False
                for i,c in enumerate(wholeplain):
                    if not c in b'1234567890abcdef' and i < wholeplain.find(b'\x00'):
                        something_Dirty = True
                        crc32IDX = i
                        crc32_seg = wholeplain[crc32IDX:crc32IDX+4]
                        if crc32_seg[3] in b'1234567890abcdef' :
                            print("CRC32 Maybe not good1")
                        wholeplain = wholeplain[:crc32IDX] + wholeplain[crc32IDX+4:]
                        break
            decr = 1
            flagEND = -1
            for i in range(5-incr):
                for idx,c in enumerate(wholeplain):
                    if not c in b'1234567890abcdef' and idx < wholeplain.find(b'\x00'):
                        crc32IDX = idx
                        crc32_seg = wholeplain[crc32IDX:crc32IDX+4]
                        if crc32_seg[3] in b'1234567890abcdef' :
                            print("CRC32 Maybe not good2")
                        wholeplain = wholeplain[:crc32IDX] + wholeplain[crc32IDX+4:]
                        break
                flagEND = wholeplain.find(b'\x00')
                if flagEND >= 32 :
                    break
                wholeplain = paddingOracle(blocks,blockIDX+offset - i ) + wholeplain

            flag = wholeplain[flagEND-32:flagEND]

            cmd = 'submit ' + flag.decode()
            conn.recv()
            conn.sendline(cmd)
            result = conn.recvuntil('\n')
            if b"OK" in result :
                print("OKKKKK!!!")
            elif b"Wrong" in result :
                print("NOOOOOOOO!!!")
                conn.close()
    except Exception as ex:
        print(ex)
        conn.close() 
        continue