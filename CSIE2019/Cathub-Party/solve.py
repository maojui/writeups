import time
import sys
import requests
import urllib.parse
from cytro import *
from cytro.sym.cbc import *
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

host = 'https://edu-ctf.csie.org:10190/'
cookies = {}
cookies['PHPSESSID'] = 'ms6h29fa741jdm3if9mhk6uf2v'
cookies['FLAG'] = urllib.parse.unquote('F%2FWITZMPKHWwO6V9XxXnSUQ1EE8dJEfNvbLTKOFizPH5NmYz%2Bv6T7l5LgDzte9tRvc2EWWJ1qKMOFzH1ZHBfAIrv9fzoFVea%2F3lVYKAWuQux1gjOafsZBSybaaH%2Bn%2Fmy')
r = requests.get(f'{host}/party.php',cookies=cookies,verify=False)

print(r.content)
# class Exploit(PaddingOracle):
    
#     def oracle(self, payload, iv, previous_resp, **kwargs):
#         cookies['FLAG'] = base64.b64encode( iv + payload ).decode()
#         cookies['FLAG'] = urllib.parse.quote(cookies['FLAG'])
#         r = requests.get(f'{host}/party.php',cookies=cookies,verify=False)
#         if (r.content.decode().endswith('get out of here.') == False) :
#             return True, None
#         else :
#             return False, None

# Encflag = cookies['FLAG']
# iv = b64d(Encflag)[:16]
# cipher = b64d(Encflag)

# key_size = 16
# exp = Exploit(key_size)
# # decrypted = exp.decrypt(ciphertext=cipher,iv=iv,is_correct=True, known_plaintext=None)
# decrypted = exp.decrypt(ciphertext=cipher,iv=iv,is_correct=True, known_plaintext=b'FLAG{EE0DF17A410C90F86E88471346B6DA77E8C878200B37E60C53E9A56913211465}\n\n\n\n\n\n\n\n\n\n')