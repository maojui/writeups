#!/usr/bin/env python2
import json
import string
from pwn import *
from os import listdir
from os.path import isfile, join

import argparse
import re
from termcolor import colored

"""
Usage :
    python m_view.py dump file
    python m_view.py peek file, id
    python m_view.py replpay file, id
"""

# like view.py
# Start with '\t' : for Received -> red
# Else : for Send -> Green
def process_raw_ascii(raw_list):
    asci = [r.strip().decode('hex') for r in raw_list ]
    for i,asc in enumerate(asci) :
        ss = ''
        for c in asc:
            if c in string.printable[:-5]:
                ss += c
            else :
                ss += '.'
        asci[i] = ss
            
    rraw = []
    for i,r in enumerate(raw_list):
        if not str(r).startswith('\t'):
            #s = ' '.join( i for i in re.findall( '..' , str(r).strip() ) )
            #rraw.append( colored( str(r).strip() , 'magenta' ) )
            #asci[i] = colored( asci[i] , 'magenta' )
            rraw.append( str(r).strip() )
            asci[i] = 'recv' + asci[i]
            #rraw.append('\033[91m' + s + '\033[00m')
            #asci[i] = '\033[91m' + asci[i] + '\033[00m'
        else :
            rraw.append(str(r).strip())
            asci[i] = 'send' + asci[i]
    return rraw,asci
    

# pwn : highlight lib address in pcap
def yuawn_filter( c ):

    mod_pools = [ '{' , '}' , '!' , '?' , ':' , '.' , ' ' , '_' ]
    hardcodes = [ 0x7f , 0xff ]
    interests = []

    # __malloc_hook , __free_hook
    # 0x3c378 main_arena top chunk offset

    printable = range( 48 , 58 ) + range( 65 , 91 ) + range( 97 , 123 )
    printable += [ ord( i ) for i in mod_pools ]

    if c == '  ':
        return c 
    elif int( c , 16 ) == 0x0a or int( c , 16 ) == 0x00:
        return colored( c , 'red' )
    elif int( c , 16 ) in hardcodes:
        return colored( c , 'grey' , 'on_green' )
    elif int( c , 16 ) not in printable:
        return colored( c , 'cyan' )
    else:
        return c


# for Yuawn's pcap analysis : raw & ascii, I don't know what happen here LoL.
def yuawn( raw , asci ):

    if len( raw ) % 32:
        r = re.findall( '.' * 32 , raw.ljust( ( len( raw  ) / 32 + 1 ) * 32 , ' '  ) )
        a = re.findall( '.' * 16 , asci.ljust( ( len( asci ) / 16 + 1 ) * 16 , '|' ) )
    else:
        r = re.findall( '.' * 32 , raw  )
        a = re.findall( '.' * 16 , asci )

    #a_remaind = a[ ( len( asci ) / 16 ) * 16 : ]

    l = 0

    for i , j in zip( r , a ):

        o = '{:08X}  '.format( l ) + '  '.join( ' '.join( yuawn_filter( j ) for j in re.findall( '..' , i ) ) for i in re.findall( '........' , i ) )
        o += '  |'
        o += '|'.join( i for i in re.findall( '....' , j ) ) + '|'

        print o
        l += 0x10


# Nice Visualization for reading pacp ... at beginning
def pprint(path,id):
    filename = path + '/' + str(id)
    with open(filename) as json_data:
        d = json.load(json_data)
        raw,asci = process_raw_ascii(d['raw'].split('\n'))
        print( '{} conversation id : {}\n'.format(d['file'],d['id']))
        for i in range(len(raw)):

            if asci[i].startswith( 'recv' ): print '[' + colored( 'Recieved' , 'red' , attrs = ['underline'] ) + ']:'
            else: print '[' + colored( 'Send' , 'green' , attrs = ['underline'] ) + ']:'

            asci[i] = asci[i][4:]

            #print(raw[i] + '\t' + asci[i])
            yuawn( raw[i] , asci[i] )

            print '\n'
        print('\n')

# Never use in competition QQ
def replay(path,id):
    # for host in targets:
        # for port_num, problem in port_map.iteritems():
        #     if problem == path:
        #         port = port_num
    path = path[path.find('/')+1:]
    host,port = path.strip().split(':')
    conn = remote(host,port)
    filename = 'extract/' + path + '/' + str(id)
    with open(filename) as json_data:
        d = json.load(json_data)
        print(d)
        for r in d['raw'].split('\n')[:-2] :
            if not str(r).startswith('\t') :
                print(str(r).decode('hex'))
                conn.send(str(r).decode('hex'))
                print(conn.recv())
        conn.interactive()
    
# Replace by stream.py
def dump(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for f in files:
        pprint(path,f)

# Replace by stream.py & view.py
def peek(path,id):
    pprint(path,id)



# args
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='avaiable subcommands')


parser_dump = subparsers.add_parser('dump', help='batch dump pcap to 8 bit data.')
parser_dump.add_argument('path', type=str, help='dump target')
parser_dump.set_defaults(func=dump)

parser_dump = subparsers.add_parser('peek', help='batch dump pcap to 8 bit data.')
parser_dump.add_argument('path', type=str, help='peek json')
parser_dump.add_argument('id', type=str, help='target id')
parser_dump.set_defaults(func=peek)

parser_replay = subparsers.add_parser('replay', help='batch dump pcap to 8 bit data.')
parser_replay.add_argument('path', type=str, help='dump target')
parser_replay.add_argument('id', type=str, help='dump id')
parser_replay.set_defaults(func=replay)


args = parser.parse_args()

if args.func == dump:
    args.func(args.path)
if args.func == peek:
    args.func(args.path, args.id)
if args.func == replay:
    args.func(args.path,args.id)
