#!/usr/bin/env python3

'''
	The sever listens to the port and monitors
	and controls traffic

'''

import os
import sys
import json
import datetime
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


def processRequest(request, connections):
	''' depending on receive/send/etc
		process request and send appropriate
		response
	'''
	response = {}
	id = None

	if 'headers' not in request:
		response['message'] = "Invalid Request"
		return response, id
	try:
		id = request['headers']['id']
	except:
		response['message'] = "Unsupported Request"
		id = None
		return response, id

	if id not in connections:
		# handle the initial addition of connnection
		try:
			conn_init = request['data']['connect']
			connections[id] = [request]
			response = {
				'connect' : "CONNECTED"
			}
		except Exception as e:
			response = {
				'connect' : False,
				'reason' : "CONNECT FIRST; " + str(e)
			}
		return response, id

	elif 'connect' in request['data']:
		# disconnected (and potentially) other
		# connection requests
		connections[id].append(request)
		conn_stat = request['data']['connect']
		if conn_stat == "DISCONNECT":
			try:
				connections.pop(id)
				response = {
					'connect' : "DISCONNECTED"
				}
			except Exception as e:
				response = {
					'connect' : "CONNECT FIRST; " + str(e)
				}
		elif conn_stat == "START":
			response = {
				'connect' : "ALREADY"
			}
		return response, id

	# other file requests
	# process main requests here
	connections[id].append(request)
	actions, targets = request['headers']['commands'], request['data']
	if "--list-files" in actions:
		response['files'] = os.listdir(config.SERVER_STORE)

	elif "--receive-files" in actions:
		files = targets
		response['files'] = files

	return response, id


def receiveConnections(sock, logger = None):
	''' main loop which controls the
		receival of requests and their
		processing
	'''
	req_count = 1
	active_connections = {}
	while 'q' not in str(input()):

		# accept an incoming request
		conn, address = sock.accept()
		d = {'host' : address[0], 'id' : address[-1]}
		l.info("R%d", req_count, extra=d)

		raw_data = conn.recv(config.buf_size)
		request = parseData(raw_data)
		print("Request")
		printJ(request)

		# process the request depending on type
		response, id = processRequest(request, active_connections)
		print("Response")
		printJ(response)

		conn.send(makeRequest(response, { 'id' : id }))
		req_count += 1

	return active_connections


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
	start_time = datetime.datetime.now().isoformat('T')
	end_connected = receiveConnections(s, logger)
	s.close()
	# display final history and store to file
	print("\n\n \033[91m Final Connection History \033[0m\n\n")
	printJ(end_connected)
	json.dump({ start_time : end_connected}, open('connections.json', 'w'))


if __name__ == '__main__':
	main()
