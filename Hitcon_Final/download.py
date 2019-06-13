import subprocess
import os

number = 163

if not os.path.exists('pcap') :
    os.makedirs('pcap')

stdoutdata = subprocess.getoutput("echo ls -l | sftp -P 2222 -i private.key doublesigma@10.10.10.21")
files = stdoutdata.split('\n')[number:]

for f in files :
    file = f.split(' ')[-1].strip()
    os.system( "echo get {} | sftp -P 2222 -i private.key doublesigma@10.10.10.21 ".format(file) )
    os.system( "xz -d {}".format(file) )
    os.system( "mv *.pcap pcap/" )


os.system( "python3 stream.py pcap/*.pcap" )
# os.system( "rm pcap/*.pcap" )