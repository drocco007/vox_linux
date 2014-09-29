import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
					level=logging.INFO)

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

import sys
sys.path.append(r'v:\IPYZMQ\bin\Debug')
clr.AddReferenceToFile('KeyIntercept.dll')

#clr.AddReferenceToFile("KeyIntercept.dll")
from KeyIntercept import KeyboardHook

from System.Threading import Thread, ThreadStart
from System.Windows.Forms import Application

from comm import zmq
import MainForm


keyboard_hook = KeyboardHook.setHook()

Application.EnableVisualStyles()
form = MainForm.MainForm()

keyboard_hook.KeyIntercepted += form.intercepted_key


# print 'SUB for control messages'
# thread = Thread(ThreadStart(form.control_thread))
# thread.Start()

Application.Run(form)

zmq.send_key('\x01Bridge exiting')
zmq.socket.Dispose()
zmq.context.Dispose()

thread.Join()
