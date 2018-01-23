import socket

port = 6009
s = socket.socket()
host = ""

s.bind((host, port))
s.listen(5)

# filename = raw_input("Enter file to share:")
print 'Server listening....'

conn, addr = s.accept()
while True:
    print 'Got connection from', addr
    f_recv = conn.recv(1024)
    # print data
    

    f = open(f_recv,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       # print('Sent ',repr(l))
       l = f.read(1024)
    f.close()
    print('Done sending')
conn.close()
