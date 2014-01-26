#!/usr/bin/env python

from plistlib import *
import  sys,os,json,uuid
import socket

HOST='0.0.0.0'
PORT=8000

tcp=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((HOST, PORT))
mdm_cmd = {}
for i in range(1, len(sys.argv)):
    arg=sys.argv[i]
    key,value=arg.split('=')
    mdm_cmd[key]=value

plist = writePlistToString(mdm_cmd)

print plist
tcp.send(plist)

tcp.close()    
