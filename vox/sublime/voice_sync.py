from contextlib import contextmanager
import os
import socket
import struct

import sublime, sublime_plugin


CLIENT_SOCK = '/var/run/user/{uid}/vox.sock'.format(uid=os.getuid())
HEADER_LENGTH = len(struct.pack('LLL', 0, 0, 0))


@contextmanager
def connect(address='/tmp/test.sock'):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    s.connect(address)

    try:
        yield s
    finally:
        s.close()


def expand_to_home(view, region):
    prefix = view.find_by_class(region.begin(), forward=False,
                                classes=sublime.CLASS_LINE_START)
    return sublime.Region(prefix, region.end())


def contextualize(view, region):
    context = expand_to_home(view, region)
    context_data = view.substr(context)

    selection_length = len(region)
    target_point = len(context) - selection_length

    return target_point, selection_length, context_data


class VoiceSyncCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        for sel in sels:
            print(sel, self.view.substr(sel))

        with connect(CLIENT_SOCK) as sock:
            target_point, selection_length, context_data = \
                contextualize(self.view, sels[0])

            text = context_data.encode('utf-8')

            message_length = HEADER_LENGTH + len(text)

            print(message_length, target_point, selection_length, context_data)

            sock.sendall(b''.join((
                struct.pack('LLL', message_length, target_point, selection_length),
                context_data.encode('utf-8'),
            )))
