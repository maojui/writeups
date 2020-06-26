
import requests
from padding_oracle import *

sess = requests.session()

# sess.cookies.set('PHPSESSID', '9d18bf8cfd2d557d8631859299f9faf1')


cipher = base64_decode("MZsC29WnQgKe+txFUj+6ZWRFDxbxdPqVPjoc2pw4K0pPHKKM3o1SNOIqm3O6v/2cWFs9Dhv0nWED723PNEEKfA==")

def oracle(cipher):
    resp = sess.post('https://turtowl.ais3.org/?action=login',
                     data={'csrf_token': base64_encode(cipher)}).text
    # assert 'Uncaught' in resp or 'Uncaught' in resp, 'Exception?'
    return 'Uncaught' not in resp


# cipher = b'[______IV______][____Block1____][____Block2____]'

# DECRYPT THE CIPHER!!!
plaintext = padding_oracle(cipher,
                           block_size=16,
                           oracle=oracle,
                           num_threads=64)