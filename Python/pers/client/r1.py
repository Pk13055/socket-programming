#!/usr/bin/env python2

import socket
import os
from sys import argv as rd
s = socket.socket()
host = "127.0.0.1"
port = int(rd[1])

s.connect((host, port))
# s.send("Hello server!")
# x = input("no. of files")
while 1:
    f_input = raw_input('enter file name: ')
    s.send(f_input);
    with open(os.path.join("Data", f_input), 'wb') as f:
        print 'file opened'
        while True:
            print('receiving data...')
            data = s.recv(1024)
            # print('data=%s', (data))
            f.write(data)
            if len(data)<1024:
                break
            # write data to a file
    f.close()
    print('Successfully get the file')
s.close()
print('connection closed')
