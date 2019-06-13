#!/usr/bin/env python2
# coding: utf-8
import subprocess as sp
import string
import re
import sys
import os
import tempfile
import argparse
import json

"""
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
TOO SLOW
"""
class PCAP:
    
    def __init__(self,path):
        self.path = path
        self.count = self.__streamCount()

    def __streamCount(self):
        p = sp.Popen('tshark -r %s -z conv,tcp | grep "<->" | wc -l' % self.path, shell=True, stdout=sp.PIPE)
        return int(p.stdout.read()) 

    def raw(self,cid):
        process = sp.Popen('tshark -r %s -z follow,tcp,raw,%d' % (self.path, cid), shell=True, stdout=sp.PIPE)
        output = process.stdout.read().decode('utf-8')
        output = output[output.find('============'):].strip('=\n')
        output = [x for x in output.strip().split('\n') if x.strip() ]
        data = '\n'.join( output[4:] )
        dest = str(output[3][output[3].rfind(' ')+1:])
        return data,dest


    def save(self,session_id,outdir):
        js = {}
        js['file'] = self.path
        js['id'] = session_id
        raw, dest = self.raw(session_id)
        js['raw'] = raw
        output = outdir + '/' + dest
        if not os.path.exists(output):
            os.makedirs(output)
        with open(output + '/' + str(session_id),'w') as f:
            f.write(json.dumps(js))
            print('Save conversation %d at %s' % (session_id,output))

def search(pcap, pattern, is_hex=False):
    data = pattern if not is_hex else pattern.decode('hex')
    flag = False
    for i in range(pcap.count):
        result = pcap.raw(i)[0].replace('\n','').replace('\t','')
        result = result.decode('hex')
        if data in result:
            flag = True
            print('\nFind \"%s\" in %s conversation %d...' % (pattern,pcap.path, i))
            pcap.save(i,'%s'%pattern)
    if not flag :
        print('Not found')

def peek(pcap,i,outdir='peek'):
    pcap.save(int(i),outdir)

def sieve(pcap, outdir='extract'):
    for i in range(pcap.count):
        pcap.save(i,outdir)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='avaiable subcommands')

parser_search = subparsers.add_parser('search', help='tranfer pattern to 9 bit data and search in pcap')
parser_search.add_argument('path', type=str, help='search target')
parser_search.add_argument('pattern', type=str, help='search pattern')
parser_search.set_defaults(func=search)


parser_peek = subparsers.add_parser('peek', help='tranfer pattern to 9 bit data and search in pcap')
parser_peek.add_argument('path', type=str, help='obj')
parser_peek.add_argument('id', type=str, help='id')
parser_peek.set_defaults(func=peek)


parser_batch = subparsers.add_parser('sieve', help='batch dump pcap to 8 bit data.')
parser_batch.add_argument('path', type=str, help='input pcap file')
parser_batch.add_argument('outdir', type=str, help='output file',default='extract',nargs='?')
parser_batch.set_defaults(func=sieve)

args = parser.parse_args()

if args.func == sieve:
    args.func(PCAP(args.path),args.outdir)
if args.func == peek:
    args.func(PCAP(args.path),args.id)
elif args.func == search:
    args.func(PCAP(args.path), args.pattern)