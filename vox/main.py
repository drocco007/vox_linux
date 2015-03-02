# coding: utf-8

import sys

import zmq

from dgram_relay import datagram_relay
from run_command import run_commands
from show_notices import show_notices
from text_buffer import manage_text_buffer
from text_relay import relay_text
from titles import broadcast_title_changes


host = '127.0.0.1'

if len(sys.argv) > 1:
    host = sys.argv[1]


print 'listening on tcp://{}:5556'.format(host)
print 'FIXME: publishing to tcp://{}:5558'.format('xpvoice')


worker_lists = [
    show_notices(host=host),
    manage_text_buffer(host=host),
    broadcast_title_changes(host=host),
    relay_text(host=host),
    run_commands(host=host),
    datagram_relay(host=host),
]

[worker.join() for worker_list in worker_lists for worker in worker_list]
