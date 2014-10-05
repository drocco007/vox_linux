# coding: utf-8

from xdo import Xdo
from xdo.xdo import CURRENTWINDOW
import zmq

from process_utils import spawn_daemon_process
import pykey


# FIXME: extract to a common module
def init_zmq(host='localhost'):
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://{}:5556'.format(host))
    socket.setsockopt(zmq.SUBSCRIBE, '')

    return socket


def is_command(message):
    #
    # FIXME: command constant for text…
    #

    command = message[0]

    return command in {'\x01', '\x11', '\x12', '\x05'}


def is_text(message):
    return not is_command(message)


def relay_text_worker(host='localhost'):
    socket = init_zmq(host=host)
    do = Xdo()

    while True:
        message = socket.recv()

        if not message or is_command(message):
            continue

        if message[0] == '\x02':
            command = message[1:]
            print '.key:', command

            if '-' in command:
                modifiers, command = command.split('-', 1)
            else:
                modifiers = ''

            pykey.send_keysym(command, modifiers)
            pykey.display.sync()
        else:
            print '.text: {} ({})'.format(message, type(message))
            do.enter_text_window(CURRENTWINDOW, message)


def relay_text(host='localhost'):
    return spawn_daemon_process(relay_text_worker, call_kw={'host': host})
