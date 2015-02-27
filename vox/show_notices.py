# coding: utf-8

import sys

from glib import GError
import pynotify

import bus
from commands import SHOW_NOTIFICATION
from process_utils import spawn_daemon_process


def notifier():
    pynotify.init(sys.argv[0])

    title = 'Dragon Naturally Speaking'
    notice = pynotify.Notification(title, '')
    notice.show()

    def show_notice(message, retry=True, notice=notice):
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

    return show_notice


def show_notice_worker(host='localhost'):
    socket = bus.connect_subscribe(host=host,
                                   subscriptions=(SHOW_NOTIFICATION,))
    show_notice = notifier()

    while True:
        try:
            message = socket.recv()[1:]
            show_notice(message)
        except:
            print 'Error showing notice:', message


def show_notices(host='localhost'):
    return [spawn_daemon_process(show_notice_worker, call_kw={'host': host})]
