import logging
import sys

logging.basicConfig(level=logging.DEBUG)

from vox import bus


if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = 'localhost'


socket = bus.connect_subscribe(host=host)

while True:
    message = socket.recv()
    logging.info('message: %s', message.decode('utf8'))
