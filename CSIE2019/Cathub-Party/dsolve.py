import time, logging
import sys
import requests
import urllib.parse
from cytro import *
from cytro.sym.cbc.PaddingOracle import *
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

sess = requests.Session()
sess.cookies['PHPSESSID'] = 'ms6h29fa741jdm3if9mhk6uf2v'

host = 'https://edu-ctf.csie.org:10190/'
cipher = 'F%2FWITZMPKHWwO6V9XxXnSUQ1EE8dJEfNvbLTKOFizPH5NmYz%2Bv6T7l5LgDzte9tRvc2EWWJ1qKMOFzH1ZHBfAIrv9fzoFVea%2F3lVYKAWuQux1gjOafsZBSybaaH%2Bn%2Fmy'


def oracle(cipher):
    
    while True:
        try:
            r = sess.get(f'{host}/party.php', cookies={'FLAG': urlencode(base64_encode(cipher))}, verify=False)
            break
        except:
            time.sleep(1)
            continue
    if (r.content.decode().endswith('get out of here.') == False) :
        return True
    else :
        return False
cipher = base64_decode(urldecode(cipher))
padding_oracle(cipher[-32:], 16, oracle, 128, log_level=logging.DEBUG)

# Encflag = cookies['FLAG']
# iv = b64d(Encflag)[:16]
# cipher = b64d(Encflag)

# key_size = 16
# exp = Exploit(key_size)
# # decrypted = exp.decrypt(ciphertext=cipher,iv=iv,is_correct=True, known_plaintext=None)
# decrypted = exp.decrypt(ciphertext=cipher,iv=iv,is_correct=True, known_plaintext=b'FLAG{EE0DF17A410C90F86E88471346B6DA77E8C878200B37E60C53E9A56913211465}\n\n\n\n\n\n\n\n\n\n')