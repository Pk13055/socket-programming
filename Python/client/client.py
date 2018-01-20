#!/usr/bin/env python3

'''
	the client sends requests for files
	and gets responses from the server

'''

import os
import sys
import json
import random
from sys import argv as rd
from time import sleep

sys.path.append(os.path.join(os.getcwd(), '..'))
import config
from utility import *

def establishConnection(socket, host, port):
	'''
	establish a connection to the server
	'''
	id = random.randint(1, config.queue_length)
	try:
		socket.connect((host, port))
		print("Reaching here")
		init_request = makeRequest({
			'connect' : "START"
			}, {'id' : id})
		print(json.dumps(parseData(init_request), indent=4))
		socket.send(init_request)
		raw_data = socket.recv(config.buf_size)
		print(json.dumps(parseData(raw_data), indent=4))
		return True, id
	except OSError as e:
		print("Connection Failed", str(e))
		return False, e.errno

def ask(socket, options):
	ques = parseArguments(options)
	print(ques)
	request = makeRequest({}, {
		'type' : "QUERY"
		})
	socket.send(request)
	response = socket.recv(config.buf_size)
	return response

def main():
	s = config.socket
	try:
		PORT = int(rd[1])
	except IndexError:
		print("Port unavailable")
		PORT = config.default_port

	stat, id = establishConnection(s, config.host, PORT)
	if not stat: sys.exit(id)
	# r = asks

if __name__ == '__main__':
	main()
