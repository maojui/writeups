
from Crypto.Cipher import AES
import header 
key = 'PHRACK-BROKENPIC'
aes = AES.new(key)

with open('brokenpic.bmp', 'rb') as f:
    data = f.read()
    pic = aes.decrypt(data)

with open('decrypt.bmp', 'wb') as f:
    f.write(header.add(pic))