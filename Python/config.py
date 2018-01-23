# configuration file for the client server

'''
	all common/global variables
	will be declared here

'''

import socket as sock
import logging
import os

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

# packet size of raw data to transfer
packet_size = 1024

# THREADS
threads = 1

# logging
logging_level = 0
log_file = os.path.join(os.getcwd(), "server.log")
FORMAT = '\033[92m%(asctime)-15s %(host)s %(id)d\033[0m %(message)s'
logging.basicConfig(level=logging_level, format=FORMAT,
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(log_file),
                    ])
logger = logging.getLogger('server')


# FILE LOCATIONS

SERVER_STORE = os.path.join(os.getcwd(), 'Data')
CLIENT_STORE = os.path.join(os.getcwd(), 'Data')

