import os
import socket
import struct

import bus
from commands import format_set_buffer_text_command
from process_utils import spawn_daemon_process


INT_LENGTH = len(struct.pack('L', 0))
BLOCK_SIZE = 4096


def _default_address():
    return '/var/run/user/{uid}/vox.sock'.format(uid=os.getuid())


def bind(address=None):
    address = address or _default_address()

    if os.path.exists(address):
        os.unlink(address)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    return s


def receive_message_length(socket, prefix=b''):
    data = bytearray(prefix)

    while len(data) < INT_LENGTH:
        data.extend(socket.recv(BLOCK_SIZE))

    length = struct.unpack('L', data[:INT_LENGTH])[0]

    return length, data


def receive_message(socket, prefix=b''):
    message_length, data = receive_message_length(socket, prefix)

    while len(data) < message_length:
        data.extend(socket.recv(BLOCK_SIZE))

    message, remainder = data[:message_length], data[message_length:]

    return message, remainder


def unpack_message(message):
    header_length = INT_LENGTH * 3
    message_length, target_point, selection_length = \
        struct.unpack('LLL', message[:header_length])

    text = message[header_length:]

    return message_length, target_point, selection_length, text


def serve_forever(zmq_host='localhost'):
    s = bind()
    remainder = b''

    out_socket = bus.connect_publish(host=zmq_host)

    while True:
        conn, client_address = s.accept()
        message, remainder = receive_message(conn, remainder)
        message_length, target_point, selection_length, text = unpack_message(message)
        print message_length, target_point, selection_length, repr(text)

        out_socket.send(format_set_buffer_text_command(text))


def datagram_relay(host='localhost'):
    return [spawn_daemon_process(serve_forever, call_kw={'zmq_host': host})]
