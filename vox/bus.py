import zmq


_context = None


def get_context():
    global _context

    if not _context:
        _context = zmq.Context()

    return _context


def get_socket(socket_type):
    return get_context().socket(socket_type)


def connect_publish(host='localhost', port=5555, scheme='tcp'):
    socket = get_socket(zmq.PUB)
    socket.connect('{}://{}:{}'.format(scheme, host, port))
    return socket


def connect_subscribe(host='localhost', subscriptions=('',), port=5556,
                      scheme='tcp'):
    socket = get_socket(zmq.SUB)
    socket.connect('{}://{}:{}'.format(scheme, host, port))

    for subscription in subscriptions:
        socket.setsockopt(zmq.SUBSCRIBE, subscription)

    return socket
