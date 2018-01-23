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
		print("Server failed to started", str(e))
		return False, e.errno


def sendFile(socket, id, files):
	'''does the actual file sending
		can using threading on this to make faster
	'''
	for file in files:
		socket.send(makeRequest({ "status" : "START" }, { 'id' : id, 'file' : file }))
		s = socket.recv(config.buf_size)
		packet_count = 0
		with open(os.path.join(config.SERVER_STORE, file), 'rb') as f:
			cur_pac = f.read(config.packet_size)
			socket.send(makeRequest({ 'raw' : cur_pac.decode('utf-8'), 'packet' : packet_count },
			 { 'id' : id, 'file' : 	file }))
			s = socket.recv(config.buf_size)
		socket.send(makeRequest({ "status" : "STOP" }, { 'id' : id, 'file' : file }))
	return True

def processRequest(socket, request, connections):
	''' depending on receive/send/etc
		process request and send appropriate
		response
	'''
	response = {}
	id = None

	# Invalid unsupported request
	if 'headers' not in request:
		response['message'] = "Invalid Request"
		return response, id
	try:
		id = request['headers']['id']
	except:
		response['message'] = "Unsupported Request"
		id = None
		return response, id

	# intial connection handling
	if id not in connections:
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

	# disconnected (and potentially) other
	# connection requests
	elif 'connect' in request['data']:
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
	active_connections, targets = request['headers']['commands'], request['data']
	if "--list-files" in actions:
		response['files'] = os.listdir(config.SERVER_STORE)

	elif "--receive-files" in actions:
		send_files = [_ for _ in targets if _ in os.listdir(config.SERVER_STORE)]
		not_sent = [_ for _ in targets if _ not in send_files]
		sendFile(socket, id, send_files)
		response['files'] = {
			'transfered' : send_files,
			'not_sent' : not_sent
		}

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

		# receive the request
		print("Request")
		raw_data = conn.recv(config.buf_size)
		request = parseData(raw_data)
		l.debug(request, extra=d)
		printJ(request)

		# process the request depending on type
		print("Response")
		response, id = processRequest(sock, request, active_connections)
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
	json.dump({ start_time : end_connected}, open('connections.json', 'a+'))


if __name__ == '__main__':
	main()
