# Python Version: 3.x
# https://pypi.python.org/pypi/cryptography

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
import hashlib 
from libnum import *

endian = 'big'
 
private = ec.generate_private_key(ec.SECP384R1(), default_backend())
px = private.public_key().public_numbers().x
py = private.public_key().public_numbers().y
header = b'0v0\x10\x06\x07*\x86H\xce=\x02\x01\x06\x05+\x81\x04\x00"\x03b\x00\x04'
my_public = header + n2s(px)+ n2s(py)

peer = [ None, None ]

def payload(data, i):
    x = s2n(data[24 : 24 + 48])
    y = s2n(data[24 + 48 :])
    prime = ec.SECP384R1()
    peer[i] = ec.EllipticCurvePublicNumbers(x, y, prime).public_key(default_backend())
    return 
 
def sha256(data):
    return hashlib.sha256(data).digest()

shared_key = [ None, None ]

def derive_keys():
    for i in range(2):
        digest = sha256(private.exchange(ec.ECDH(), peer[i]))
        shared_key[i] = Cipher(algorithms.AES(digest), modes.CBC(b'0000000000000000'), default_backend())

def run_crypto(cryptor, data):
    buf = bytearray(4098)
    len_crypted = cryptor.update_into(data, buf)
    return bytes(buf[: len_crypted]) + cryptor.finalize()
 
def mitm(data):
    data = run_crypto(shared_key[0].decryptor(), data)
    print(data)
    data = run_crypto(shared_key[1].encryptor(), data)
    return data
 
def decrypt(data):
    data = run_crypto(shared_key[1].decryptor(), data)
    print(data)
 