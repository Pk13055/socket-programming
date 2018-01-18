#!/usr/bin/env python3

'''
	The sever listens to the port and monitors
	and controls traffic

'''

import os
import sys
import json
from time import sleep
from sys import argv as rd

sys.path.append(os.path.join(os.getcwd(), '..'))
import config
from utility import *
from config import logger as l

def startServer(socket, host, port):
	# bind to the given socket to begin listening
	# for connections
	try:
		socket.bind((config.host, port))
		socket.listen(config.queue_length)
		l.debug("Server started at '%s' : %d", host, port,
			extra={'host' : config.host, 'id' : 0})
		return True, None
	except Exception as e:
		l.error("Server failed to start", str(e))
		return False, e.errno


def processRequest(request):
	''' depending on receive/send/etc
		process request and send appropriate
		response
	'''
	response = {}
	return response


def receiveConnections(sock, logger = None):
	''' main loop which controls the
		receival of requests and their
		processing
	'''

	req_count = 1
	while 'q' not in str(input()):

		# accept an incoming request
		conn, address = sock.accept()
		d = {'host' : address[0], 'id' : address[-1]}
		l.info("R%d", req_count, extra=d)

		raw_data = conn.recv(config.buf_size)
		request = parseData(raw_data)
		if 'headers' in request:
			l.info(request['headers'], extra=d)
			print(json.dumps(request['data'], indent=4))
		else:
			print(json.dumps(request, indent=4))

		# process the request depending on type
		response = processRequest(request)

		conn.send(makeRequest(response, {'status' : True}))
		req_count += 1


def main():
	# socket to bind to for communication
	s = config.socket
	try:
		PORT = int(rd[1])
	except IndexError:
		PORT = config.default_port

	# starts the server and handles any port, etc issues
	status, logger = startServer(s, config.host, PORT)
	if not status: sys.exit(logger)

	# begin the loop to accept connections
	receiveConnections(s, logger)


if __name__ == '__main__':
	main()
