__all__ = ['manage_text_buffer']


# from geventwebsocket import WebSocketServer, WebSocketApplication, Resource

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import zmq

from process_utils import spawn_daemon_process


COMMAND_BROADCAST_TITLE='\x05'
COMMAND_MANAGE_BUFFER = '\x12'
COMMAND_CLEAR_BUFFER = '\x1a'
COMMAND_SET_BUFFER_TEXT = '\x02'
RECORD_SEPARATOR='\x1e'


def init_zmq(host='localhost', init_in=True, init_out=True):
    context = zmq.Context()
    in_socket = out_socket = None

    if init_in:
        in_socket = context.socket(zmq.SUB)
        in_socket.connect('tcp://{}:5556'.format(host))
        in_socket.setsockopt(zmq.SUBSCRIBE, COMMAND_BROADCAST_TITLE)

    if init_out:
        out_socket = context.socket(zmq.PUB)
        out_socket.connect('tcp://{}:5555'.format(host))

    return context, in_socket, out_socket


def manage_buffer_on_app_switch(host='localhost'):
    context, _in, _out = init_zmq(host=host)

    while True:
        message = _in.recv()
        _out.send(''.join((COMMAND_MANAGE_BUFFER, COMMAND_CLEAR_BUFFER)))


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

    application.listen(5557,
     ssl_options={
        "certfile": "voice_relay.crt",
        "keyfile": "voice_relay.key",
    }
    )

    tornado.ioloop.IOLoop.instance().start()

def chrome_socket_server(host='localhost'):
    socket = init_zmq(host=host, init_in=False)[2]

    class ChromeNamespace(BaseNamespace):
        def recv_message(self, message):
            print "PING!!!", message
            message, _ = message.split('{}')

            print
            print map(ord, message)
            print


            socket.send_string(u''.join((COMMAND_MANAGE_BUFFER,
                                         COMMAND_SET_BUFFER_TEXT,
                                         message)))


    def bind_chrome(environ, start_response):
        if environ['PATH_INFO'].startswith('/socket.io'):
            return socketio_manage(environ, { '': ChromeNamespace })
        else:
            return HTTP404(environ, start_response)


    def HTTP404(environ, start_response):
        start_response('404 NOT FOUND', [])
        yield 'File not found'


    sio_server = SocketIOServer(
        ('', 5557), bind_chrome,
        policy_server=False)
    sio_server.serve_forever()


def manage_text_buffer(host='localhost'):
    # import signal
    # signal.signal(signal.SIGINT, signal.SIG_DFL)

    spawn_daemon_process(ss, call_kw={'host': host})
    return spawn_daemon_process(manage_buffer_on_app_switch,
                                call_kw={'host': host})
