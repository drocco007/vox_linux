import sys

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

    # FIXME: a bit of a hack, this...
    if message == '\x01Bridge exiting':
        sys.stdout.flush()
        sys.stdout.close()
        break

    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()