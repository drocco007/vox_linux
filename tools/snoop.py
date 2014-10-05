import logging
import sys

logging.basicConfig(level=logging.DEBUG)

import zmq

if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = 'localhost'


context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://{}:5556".format(host))
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    message = socket.recv()
    logging.info('message: %s', message.decode('utf8'))
