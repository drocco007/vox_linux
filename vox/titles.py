import gtk
import wnck
import zmq

from process_utils import spawn_daemon_process


COMMAND_BROADCAST_TITLE='\x05'
RECORD_SEPARATOR='\x1e'


def init_zmq(host='localhost'):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect('tcp://{}:5555'.format(host))
    return socket


def translate(application_name):
    app_name = application_name.lower()
    if 'pycharm' in app_name:
        return 'pycharm'
    elif 'chrom' in app_name:
        return 'google_chrome'
    else:
        return application_name


def sniff_titles(screen=None, host='localhost'):
    screen = screen or wnck.screen_get_default()
    socket = init_zmq(host=host)

    def app_changed(screen, previous_window, *data):
        try:
            window = screen.get_active_window()
            application = translate(window.get_application().get_name())

            payload = '{}{}{}{}'.format(COMMAND_BROADCAST_TITLE,
                                        window.get_name(),
                                        RECORD_SEPARATOR,
                                        application)

            socket.send(payload)
        except:
            pass

    screen.connect('active-window-changed', app_changed)

    gtk.main()


def broadcast_title_changes(host='localhost'):
    # import signal
    # signal.signal(signal.SIGINT, signal.SIG_DFL)

    return spawn_daemon_process(sniff_titles, call_kw={'host': host})


def stop():
    gtk.main_quit()