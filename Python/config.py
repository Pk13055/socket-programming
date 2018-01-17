# configuration file for the client server

'''
	all common/global variables
	will be declared here

'''

import socket as sock

# default port in case port is not specified
default_port = 8080

# main socket that will be used for our connection
socket = sock.socket()

# host (localhost)
host = '127.0.0.1'

# default number of queued requests to the server
queue_length = 10

# buffer size

buf_multiple = 4096
# set only the multiplier
buf_multiplier = 1

# the incoming message size can atmost be of this size
buf_size = buf_multiplier * buf_multiple

# THREADS
threads = 1
