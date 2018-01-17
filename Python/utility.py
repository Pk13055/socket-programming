# utility file

'''
	file that contains utility functions used across
	the board
'''
import json
import os
import sys

def parseData(data):
	'''
		parses the request into pythonic
		(JSON) representation
	'''
	if isinstance(data, bytes):
		data = data.decode('utf-8')
	try:
		data = json.loads(data)
	except:
		data = data.split('\n\r\n')
		if len(data) == 2:
			# browser or curl request
			headers, data = data
			data = {
				'headers' : headers.splitlines(),
				'data' : data
			}
		else:
			data = { 'data' : data }
			data = data['data'].strip(' ').strip('\n').strip(' ')
	try:
		data['data'] = json.loads(data['data'])
	except:
		pass
	return data

def makeRequest(data, headers = None):
	''' convert the request into a json
		byte array
	'''
	response = {}
	if headers is not None:
		response['headers'] = headers
	response['data'] = data
	json_rep = json.dumps(response).encode('utf-8')
	return bytes(json_rep)
