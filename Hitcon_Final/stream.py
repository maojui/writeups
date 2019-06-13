
import dpkt
import argparse
from urllib.parse import unquote
import os, sys
import hashlib

hash = lambda sport, dport: hashlib.md5('-'.join(map(str,sorted([sport,dport]))).encode('utf-8')).hexdigest()
my_ip = '10.0.12.1'
my_ip = ''.join(map(lambda x: hex(x)[2:].rjust(2,'0'),map(int,my_ip.split('.'))))

class stream:
    
    Count = 1
    
    def __init__(self, pcap, source, destination):
        self.pcap = pcap
        self.sport = source         # from attacker's or my random port out
        self.dport = destination    # vulnerable port connect
        self.count = stream.Count
        stream.Count += 1
        self.conversation = []

    # Make bytes to strings, take out b'\x00A\x19' ->  \x00A\x19
    def preprocess(self,content):
        if self.sport == 80 or self.dport == 80 :
            return unquote(str(content)[2:-1])
        else :
            return str(content)[2:-1]

    # save the content to each stream class.
    def add_content(self,ip):
        self.mine = True if my_ip == hex(int.from_bytes(ip.src,'big'))[2:].rjust(8,'0') else False
        tcp = ip.data
        if tcp.sport == self.sport :
            return self.conversation.append(self.preprocess(tcp.data))
        elif tcp.sport == self.dport :
            return self.conversation.append('\t'+self.preprocess(tcp.data))
        else :
            print("WTF")
            return self.conversation.append('\t'+self.preprocess(tcp.data))

    # write out to file.
    def save(self):
        dd = self.pcap.rstrip('.pcap')
        os.makedirs(dd,exist_ok=True)
        
        # if self.mine:
        #     filename = '/'.join(map(str,[self.dport,self.sport]))
        #     os.makedirs(os.path.join(dd,'mine'),exist_ok=True)
        #     os.makedirs(os.path.join(dd,'mine',str(self.dport)),exist_ok=True)
        #     with open(os.path.join(dd,'mine',filename),'w') as f :
        #         f.write('\n'.join(self.conversation))
        #     return 

        if self.dport in [80,8000,9487,2323,56746] :  # filter my attack
            filename = '/'.join(map(str,[self.dport,self.sport]))
            os.makedirs(os.path.join(dd,str(self.dport)),exist_ok=True)
            with open(os.path.join(dd,filename),'w') as f :
                f.write('\n'.join(self.conversation))
        else :                                        # Maybe is our attack, confuse, .... 
            filename = '/'.join(map(str,[self.sport,self.dport]))
            os.makedirs(os.path.join(dd,'??'),exist_ok=True)
            os.makedirs(os.path.join(dd,'??',str(self.sport)),exist_ok=True)
            with open(os.path.join(dd,'??',filename),'w') as f :
                f.write('\n'.join(self.conversation))


def extract(pcap):
    # pcap ='pcap/2017-12-08_16:54:21.pcap'
    payload = []
    streams = {}
    key = ''

    for ts, pkt in dpkt.pcap.Reader(open(pcap,'rb')):

        eth = dpkt.ethernet.Ethernet(pkt) 
        if eth.type!=dpkt.ethernet.ETH_TYPE_IP :
            continue

        ip = eth.data
        tcp = ip.data
        
        # print(str(ip.dst))
        
        if ip.p == dpkt.ip.IP_PROTO_TCP and tcp.data != b'': 
            
            key = hash(tcp.sport,tcp.dport)
            try :
                streams[key].add_content(ip)
            except :
                streams[key] = stream(pcap,tcp.sport,tcp.dport)
                streams[key].add_content(ip)

    for ss in streams.values():
        ss.save()



if __name__ == "__main__":
    
    for file in sys.argv[1:] :
        
        extract(file)
        print(file," Extracted.")