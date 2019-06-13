import sys
import argparse

flag = 0

# Start with '\t' : [Received]
# Else : [Send]

def view(line):
    global flag
    if flag == 0 :
        if line.startswith('\t') :
            flag ^= 1
            print('\n[Received]')
        else :
            print(line)
    if flag == 1 :
        if not line.startswith('\t') :
            flag ^= 1
            print('\n[Send]')
            view(line)
        else :
            print(line)

if __name__ == "__main__":
    print('\n[Send]')
    with open(sys.argv[1],'r') as f:
        for line in f.readlines():
            view(line)