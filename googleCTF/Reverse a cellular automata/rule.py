import subprocess

rule126 = {
    '000' : '0',
    '001' : '1',
    '010' : '1',
    '011' : '1',
    '100' : '1',
    '101' : '1',
    '110' : '1',
    '111' : '0',
}

def _rule126(_in):
    # binstr = bin(_in)[2:].rjust(32,'0')
    binstr = _in
    binstr = binstr[-1:] + binstr + binstr[:2]
    _out = ''
    for i in range(len(binstr)-3) :
        _out += rule126[binstr[i:i+3]]
    return hex(int(_out,2))


def reverse(_in,_out):
    binstr = bin(_in)[2:].rjust(32,'0')

    binstr = binstr[-1:] + binstr + binstr[:2]
    _out = ''
    for i in range(len(binstr)-3) :
        _out += rule126[binstr[i:i+3]]
    return hex(int(_out,2))

# 0110011011011110001111000001101111111000011111111101111111001111

# def reversebit(idx, cur, target):
    


cur = ['00','11']

target = '0110011011011110001111000001101111111000011111111101111111001111'
# target = '01110011111111111110001110111000'
idx = 0
res = set()

def reversebit(idx,cur,target):
    if idx == len(target) :
        if cur[-1] == cur[0]:
            if _rule126(cur[1:-1]) == '0x66de3c1bf87fdfcf':
                res.add(cur[1:-1])
        return 
    for b in ['0','1'] :
        cand = cur[-2:] + b
        if rule126[cand] == target[idx]:
            reversebit(idx+1,cur + b,target)

for c in cur :
    reversebit(idx,c,target)


for r in res:
    key = hex(int(r,2))[2:]
    flag = "U2FsdGVkX1/andRK+WVfKqJILMVdx/69xjAzW4KUqsjr98GqzFR793lfNHrw1Blc8UZHWOBrRhtLx3SM38R1MpRegLTHgHzf0EAa3oUeWcQ="
    p = subprocess.Popen(f'echo "{key}" > /tmp/plain.key;', stdout=subprocess.PIPE)
    p = subprocess.Popen(f'xxd -r -p /tmp/plain.key > /tmp/enc.key;', stdout=subprocess.PIPE)
    p = subprocess.Popen(f'echo "{flag}" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:/tmp/enc.key;', stdout=subprocess.PIPE)
    result = p.communicate()[0]
    print(result)





