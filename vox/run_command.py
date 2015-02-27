# coding: utf-8

import shlex
from subprocess import Popen
import sys

import bus
from commands import RUN_COMMAND
from process_utils import spawn_daemon_process


def run_command_worker(host='localhost'):
    socket = bus.connect_subscribe(host=host, subscriptions=(RUN_COMMAND,))

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
