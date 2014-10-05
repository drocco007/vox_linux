# coding: utf-8

import time
import shlex
from subprocess import Popen
import sys

import pynotify
from glib import GError

import zmq

from text_buffer import manage_text_buffer
from text_relay import relay_text
from titles import broadcast_title_changes


host = '127.0.0.1'

if len(sys.argv) > 1:
    host = sys.argv[1]


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://{}:5556'.format(host))
socket.setsockopt(zmq.SUBSCRIBE, '')

print 'listening on tcp://{}:5556'.format(host)
print 'FIXME: publishing to tcp://{}:5558'.format('xpvoice')

pynotify.init(sys.argv[0])

title = 'Dragon Naturally Speaking'
notice = pynotify.Notification(title, '')
notice.show()

def show_notice(message, retry=True):
    global notice

    try:
        if not pynotify.is_initted():
            pynotify.init(sys.argv[0])

        if not notice:
            notice = pynotify.Notification(title, message)
        else:
            notice.update(title, message)

        notice.show()
    except GError:
        # libnotify's documentation is… awful. This song and dance is required
        # because at some point in the process lifecycle pynotify loses its
        # connection and raises. Disconnecting and reestablishing the
        # connection gets things back on track.
        notice = None
        pynotify.uninit()

        if retry:
            show_notice(message, False)


manage_text_buffer(host=host)
broadcast_title_changes(host=host)
relay_text(host=host)


while True:
    message = socket.recv()

    if not message: continue

    message = message.decode('utf-8')

    #
    # FIXME: constant module
    #
    if message[0] == '\x01':
        message = message[1:]
        print '.message', message

        show_notice(message)
    elif message[0] == '\x11':
        command = message[1:]
        print '.command:', command
        Popen(shlex.split(command))
    elif message[0] in {'\x12', '\x05', '\x02'}:
        # print 'control message', message[1:]
        pass
    #
    # FIXME: command constant for text
    #
    # else:
       #  # import pdb; pdb.set_trace()
       #  print '.text: {} ({})'.format(message, type(message))

       #  pykey.send_string(unicode(message))

