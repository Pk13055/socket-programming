#!/usr/bin/env python3

import socket

port = 60001
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

filename = str(input("Enter file to share:"))
print('Server listening....')

while True:
    conn, addr = s.accept()
    print('Got connection from', addr)
    data = conn.recv(10)
    print(data)
    print('Server received', repr(data))

    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print('Done sending')
    conn.send(b'Thank you for connecting')
    conn.close()
    break
