# coding: utf-8

import shlex
from subprocess import Popen
import sys

import zmq

from commands import RUN_COMMAND
from process_utils import spawn_daemon_process


def init_zmq(host='localhost'):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://{}:5556'.format(host))
    socket.setsockopt(zmq.SUBSCRIBE, RUN_COMMAND)

    return socket


def run_command_worker(host='localhost'):
    socket = init_zmq(host=host)

    while True:
        message = socket.recv()

        if not message: continue

        message = message.decode('utf-8')

        if message[0] == '\x11':
            command = message[1:]
            print '.command:', command
            Popen(shlex.split(command))


def run_commands(host='localhost'):
    return [spawn_daemon_process(run_command_worker, call_kw={'host': host})]
