#!/usr/bin/env python3

'''
	The sever listens to the port and monitors
	and controls traffic

'''

import os
import sys
import socket as sock
import json
from time import sleep
from sys import argv as rd

sys.path.append(os.path.join(os.getcwd(), '..'))
import config
from utility import *

def startServer(socket, host, port):
	# bind to the given socket to begin listening
	# for connections
	try:
		socket.bind((config.host, port))
		socket.listen(config.queue_length)
		print("Server started at '%s' : %d"
			% (host, port))
		return True, None
	except Exception as e:
		print("Server failed to start", str(e))
		return False, e.errno


def receiveConnections(sock):
	while True:
		conninfo, addr = sock.accept()
		raw_data = conninfo.recv(config.
			buf_size).decode('utf-8')
		data = parseData(raw_data)
		print(json.dumps(data, indent=4))
		sleep(0.5)

def main():
	s = config.socket
	try:
		PORT = int(rd[1])
	except IndexError:
		PORT = config.default_port

	# starts the server and handles any port, etc issues
	status, code = startServer(s, config.host, PORT)
	if not status: sys.exit(code)
	# begin the loop to accept connections
	receiveConnections(s)


if __name__ == '__main__':
	main()
