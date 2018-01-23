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

def establishConnection(socket, host, id, port, typ):
	'''
	establish a connection to the server
	'''
	try:
		socket.connect((host, port))
		if typ:
			connexion = "START"
		else:
			connexion = "DISCONNECT"
		init_request = makeRequest({
			'connect' : connexion
			}, {'id' : id})
		printJ(parseData(init_request))
		socket.send(init_request)
		raw_data = socket.recv(config.buf_size)
		response = parseData(raw_data)
		print("Response : ")
		printJ(response)
		if 'connect' in response['data']:
			if "CONNECT" in response['data']['connect']:
				return True, id
			elif response['data']['connect'] == "ALREADY":
				return True, None
		else:
			raise OSError
	except OSError as e:
		print("Connection Failed", str(e))
		return False, e.errno

def receiveFiles(socket, id):
	''' function to receive the files requested
	'''
	file_list = []
	"""
		# RECEIVE START REQ
		# SEND okay
		# Receive x Number of packets
		# SEND OKAY FOR EACH
		# RECEIVE STOP REQ
		# SEND okay
	"""
	init_req = socket.recv(config.buf_size)
	request = parseData(init_req)
	printJ(request)
	# send receive
	while True:
		init_req = socket.recv(config.buf_size)
		request = parseData(init_req)
		printJ(request)
		# handle start stop here
		if 'status' in request['headers']:
			cur_status = request['headers']['status']
			if cur_status == "START":
				pass
			elif cur_status == "STOP":
				pass
		elif 'files' in request['data']:
			# handle the complete transfer of files
			break
	return False

def ask(socket, id, options, host, port):
	socket.connect((host, port))
	request = parseArguments(options, id)
	print("Request : ")
	printJ(request)
	socket.send(makeRequest(request))
	if "--receive-files" in request['headers']['commands']:
		print("Receiving Files")
		receiveFiles(socket, id)
	response = socket.recv(config.buf_size)
	return parseData(response)

def main():
	s = config.socket
	try:
		PORT = int(rd[1])
	except IndexError:
		print("Port unavailable")
		PORT = config.default_port
	try:
		id = int(rd[2])
	except:
		id = random.randint(1, config.queue_length)

	# other mechanism for non-persistent
	if "-non-persistent" in rd:
		return True

	# to establish the initial connection
	# persistent connection by default
	if "-connect" in rd or "-disconnect" in rd:
		typ = "-connect" in rd
		stat, id = establishConnection(s, config.host, id, PORT, typ)
		if not stat: sys.exit(id)
	elif "-connected" in rd:
		resp = ask(s, id, rd, config.host, PORT)
		print("Response : ")
		printJ(resp)
		return True
	else:
		print("Every request must be -connected or -connect type")
		return False



if __name__ == '__main__':
	main()
