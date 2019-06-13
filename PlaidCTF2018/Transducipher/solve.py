from transducipher import *

T = [
    ((2, 1), 1),
    ((5, 0), 0),
    ((3, 4), 0),
    ((1, 5), 1),
    ((0, 3), 1),
    ((4, 2), 0),
]

data = [[13079742441184578626, 15822063786926281121],
    [13416567443684297300, 1953576081095923750],
    [4616590709284765790, 12242300051344248099],
    [8927700908577296018, 9212645445239734194],
    [7046689723092979039, 14605811860901350724],
    [11723181797717683420, 4856237318714098520],
    [462956565916497673, 11917849788719540909],
    [15062759243211353209, 1178676016977386894],
    [5006958167746643506, 12231044178199617742],
    [17215578442192296916, 7867686081879292369],
    [3264652127960099870, 11088704409660527687],
    [67438940002497203, 13146678993523844395],
    [10567909756016925586, 16545327010848548669],
    [15707806635548046505, 14743926144157706447],
    [6478276705282625651, 18007098612493695685],
    [10970386673164693022, 12683515533170128309]]
 

din = []
dout = []
for d in data :
    din.append( block2bin(d[0]) )
    dout.append( block2bin(d[1]) )

def bitTransduce(b0,state=0):
    ns, b = T[state]
    return b0 ^ b, ns[b0]

keys = set()
possibleKey = set()
def guess_key(idx, input, output, guess_states, key):
    states = guess_states
    if idx == BLOCK_SIZE//2:
        states = [states[0],(0,0),states[2],(0,0),states[4],(0,0)]
    elif idx == BLOCK_SIZE:
        possibleKey.add( bin2block(key) )
        return key
    for b0 in (0,1):
        key_pass = [k for k in key]
        next_states = []
        key_tmp = b0
        data_tmp = input[idx]
        for ds, ks in states :
            data_tmp = data_tmp ^ key_tmp
            data_tmp, dstate = bitTransduce(data_tmp, state=ds)
            key_tmp, kstate = bitTransduce(key_tmp, state=ks)
            next_states.append((dstate,kstate))
        if data_tmp == output[idx] :
            key_pass.append(b0)
            guess_key(idx+1,input,output,next_states,key_pass)

flag = 0
for i in range(len(data)):
    counter = 0
    possibleKey = set()
    for k in range(6**5):
        counter += 1
        a,b,c,d,e = [(k // (6**j)) % 6 for j in range (5)]
        states = [(0,0),(a,b),(0,0),(c,d),(0,0),(e,0)]
        tmp = guess_key(0,din[i],dout[i],states,[])
        if counter % 1000== 0:
            print(counter)
    if possibleKey != set() :
        if keys == set() :
            keys = possibleKey.copy()
        keys.intersection_update(possibleKey)
        print(keys)
    if len(keys) < 1000:
        findKey = False
        for k in keys :
            C = Transducipher(k)
            if C.encrypt(bin2block(din[0])) == bin2block(dout[0]):
                findKey = True
                flag = hex(k)[2:]
                break
        if findKey :
            print('\nThe flag is PCTF{%s}' % flag)
            break

    print(len(keys))

# Flag : {11424187353095200768, 11424187353095200769}
