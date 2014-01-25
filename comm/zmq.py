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


def send_key(key):
	socket.Send(key, Encoding.UTF8)


def send_command(text):
	print 'command', text
	send_key('\x02' + text)
