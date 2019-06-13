import subprocess

flag = ''

for i in range(100):
    
    a = subprocess.check_output(['curl','-I',f'http://104.199.235.135:31331/index.php?p={i}'],)
    idx = a.find(b'Partial-Flag: ')
    flag += chr(a[idx+len(b'Partial-Flag: ')])


print(flag,)

# AIS3{g00d! u know how 2 check H3AD3R fie1ds.}