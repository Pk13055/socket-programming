#!/usr/bin/env python3

'''
	the client sends requests for files
	and gets responses from the server

'''


import os
import sys
import socket as sock
import json
import random
from sys import argv as rd

sys.path.append(os.path.join(os.getcwd(), '..'))
import config
from utility import *

def connectToServer(socket, host, port):
	'''
	establish a connection to the server
	'''
	id = random.randint(1, config.queue_length)
	try:
		socket.connect((host, port))
		req = makeRequest({'id' : id}, {'status' : True })
		socket.send(req)
		return True, id
	except OSError as e:
		print("Connection Failed", str(e))
		return False, e.errno


def main():
	s = config.socket
	try:
		PORT = int(rd[1])
	except IndexError:
		PORT = config.default_port

	stat, id = connectToServer(s, config.host, PORT)
	if not stat: sys.exit(id)

if __name__ == '__main__':
	main()
