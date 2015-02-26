# coding: utf-8

import shlex
from subprocess import Popen
import sys

import zmq

from show_notices import show_notices
from text_buffer import manage_text_buffer
from text_relay import relay_text
from titles import broadcast_title_changes


host = '127.0.0.1'

if len(sys.argv) > 1:
    host = sys.argv[1]


show_notices(host=host)
manage_text_buffer(host=host)
broadcast_title_changes(host=host)
relay_text(host=host)


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://{}:5556'.format(host))
socket.setsockopt(zmq.SUBSCRIBE, '\x11')

print 'listening on tcp://{}:5556'.format(host)
print 'FIXME: publishing to tcp://{}:5558'.format('xpvoice')

while True:
    message = socket.recv()

    if not message: continue

    message = message.decode('utf-8')

    if message[0] == '\x11':
        command = message[1:]
        print '.command:', command
        Popen(shlex.split(command))
