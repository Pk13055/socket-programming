import socket

host = ""
port = 60001

while 1:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((host, port))
    s.listen(5)

    print 'Server listening....'

# while True:
    conn, addr = s.accept()
    print 'Connection with client formed'
    filename = conn.recv(1024)
    print filename
    # print('Server received', repr(data))

    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       # print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    print('Done sending')
    conn.close()
    s.close()
