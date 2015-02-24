__all__ = ['manage_text_buffer']


import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import zmq

from commands import BROADCAST_APPLICATION_TITLE, CLEAR_BUFFER_COMMAND
from process_utils import spawn_daemon_process


def init_zmq(host='localhost', init_in=True, init_out=True):
    context = zmq.Context()
    in_socket = out_socket = None

    if init_in:
        in_socket = context.socket(zmq.SUB)
        in_socket.connect('tcp://{}:5556'.format(host))
        in_socket.setsockopt(zmq.SUBSCRIBE, BROADCAST_APPLICATION_TITLE)

    if init_out:
        out_socket = context.socket(zmq.PUB)
        out_socket.connect('tcp://{}:5555'.format(host))

    return context, in_socket, out_socket


def manage_buffer_on_app_switch(host='localhost'):
    context, _in, _out = init_zmq(host=host)

    while True:
        message = _in.recv()
        _out.send(CLEAR_BUFFER_COMMAND)


def ss(host='localhost'):
    class EchoHandler(tornado.websocket.WebSocketHandler):
        def check_origin(self, origin):
            return True

        def open(self):
            print "Connection opened"

        def on_message(self, message):
            print "MESSAGE FOR YOU SIR!", message
            self.write_message(message)

        def on_close(self, ):
            print 'Connection closed'

    application = tornado.web.Application([
        (r'/', EchoHandler),
    ])

    application.listen(5557, ssl_options={
        "certfile": "voice_relay.crt",
        "keyfile": "voice_relay.key",
    })

    tornado.ioloop.IOLoop.instance().start()


def manage_text_buffer(host='localhost'):
    spawn_daemon_process(ss, call_kw={'host': host})
    return spawn_daemon_process(manage_buffer_on_app_switch,
                                call_kw={'host': host})
