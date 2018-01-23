# utility file

'''
	file that contains utility functions used across
	the board
'''
import json
import shlex
import os
import sys


def printJ(resp):
    if isinstance(resp, dict):
        print(json.dumps(resp, indent=4))
    else:
        print(resp)


def parseArguments(argv, id):
    ''' parse the command line arguments
    '''
    response = {
        'headers': {
        	'id' : id,
        	'commands' : list(filter(lambda x: x[:2] == "--", argv))
    	},
        'data': [_[1:] for _ in list(filter(lambda x: x[0] == "@", argv))]
    }
    return response


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
                'headers': headers.splitlines(),
                'data': data
            }
        else:
            data = {'data': data}
            if isinstance(data['data'], str):
                data = data['data'].strip(' ').strip('\n').strip(' ')
    try:
        data['data'] = json.loads(data['data'])
    except:
        pass
    return data


def makeRequest(data, headers=None):
    ''' convert the request into a json
            byte array
    '''
    response = {}
    if headers is None and 'headers' in data:
        response = data
    elif headers is not None:
        response['headers'] = headers
        response['data'] = data
    json_rep = json.dumps(response).encode('utf-8')
    return bytes(json_rep)
