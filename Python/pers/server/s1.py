#!/usr/bin/env python2

import socket
import os
from sys import argv as rd
s = socket.socket()
host = "127.0.0.1"
port = int(rd[1])

s.bind((host, port))
s.listen(10)

# filename = raw_input("Enter file to share:")
print 'Server listening....'

conn, addr = s.accept()
while True:
    print 'Got connection from', addr
    f_recv = conn.recv(1024)
    # print data


    f = open(os.path.join("Data", f_recv),'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       # print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    print('Done sending')
conn.close()
