import clr

clr.AddReferenceToFile("clrzmq.dll")
from System.Text import Encoding
import ZMQ as zmq
from ZMQ import SocketType

context = zmq.Context(1)
socket = context.Socket(SocketType.PUB)


print "Opening pub socket..."
socket.Bind("tcp://*:5556")

#for request in range(1,10):
#    print "Sending request ", request,"..."
#    socket.Send("Hello", Encoding.ASCII)
#
#    message = socket.Recv(Encoding.ASCII)
#    print "Received reply ", request, "[", message, "]"

def send_text(text):
	pass

def send_key(key):
#	print key, type(key), hex(unicode(key).encode('utf-8'))
	socket.Send(key, Encoding.UTF8)
	

def send_command(text):
	send_key('\x02' + text)