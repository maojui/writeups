
# import threading
# import time
# from communicate import *


# class myThread (threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
        
#     def run(self):
#         getFlag()


# # import json
# # icoAdd = '0xca5Fd825c4B30D445C37a323606df7f68aF70046'
# # password = '12345'
# # wallet = '0xB0E9f4C629C86c921812ee2cB60d02C1f7405d89'

# # contractAddresses = json.loads(get_victim(wallet))
# # tokAdd = contractAddresses['token']
# # icoAdd = contractAddresses['ico']

# owner = '0x32fe35D5F655c0aB47F3C1D140d3b7f95C637403'
# icoContract = ICO(icoAdd, wallet, password, ico_abi)
# tokenContract = Token(icoAdd, wallet, password, token_abi)


# def getFlag() :
#     print(get_flag(icoAdd,wallet,password))

# tt = [myThread() for c in range(30)]

# for t in tt :
#     t.start()
#     time.sleep(1)

# for t in tt :
#     t.join()

