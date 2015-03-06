import clr

clr.AddReferenceToFile("clrzmq.dll")

from System import AppDomain
from System.Text import Encoding

import ZMQ as zmq
from ZMQ import SocketType

context = zmq.Context(1)
socket = context.Socket(SocketType.PUB)


print "Opening pub socket..."
socket.Connect('tcp://vmhost:5555')


def send_text(text):
	pass

# FIXME: these names are terrible
# FIXME: pull in predefined constants
def send_key(key):
    socket.Send('\x03' + key, Encoding.UTF8)


def send_command(text):
    socket.Send('\x02' + text, Encoding.UTF8)


def notify(text):
	socket.Send('\x01' + text, Encoding.UTF8)
