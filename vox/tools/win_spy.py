#!/usr/bin/python
import signal
from subprocess import Popen

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11


class WinSpy(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Vox Win Spy')
        self.init_components()
        self.connect_listeners()
        self.set_defaults()
        self.position_window()

    def init_components(self):
        self.label = Gtk.Label('')
        self.add(self.label)

    def connect_listeners(self):
        self.connect('show', self.on_show)

    def set_defaults(self):
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_gravity(Gdk.Gravity.SOUTH_EAST)

        self.set_default_size(400, 768)

    def position_window(self):
        width, height = self.get_size()
        screen = self.get_screen()
        self.move(screen.get_width() - width, screen.get_height() - height)

    def on_show(self, widget):
        self.xid = hex(self.get_window().get_xid())
        self.label.set_text(self.xid)
        print self.xid
        self.win_connect()

    def win_connect(self):
        Popen(['xfreerdp', '-K', '-X', self.xid, 'voicehost'])


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    win = WinSpy()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()

    Gtk.main()


if __name__ == '__main__':
    main()
