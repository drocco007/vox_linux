import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
					level=logging.INFO)

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

clr.AddReferenceToFile('KeyIntercept.dll')

from KeyIntercept import KeyboardHook

from System.Threading import Thread, ThreadStart
from System.Windows.Forms import Application

from comm import zmq
import MainForm


# initialize the keyboard intercept hook to capture Alt/Win key chords
keyboard_hook = KeyboardHook.setHook()

Application.EnableVisualStyles()
form = MainForm.MainForm()


# Notify the form when a key is intercepted
keyboard_hook.KeyIntercepted += form.intercepted_key


Application.Run(form)


# Clean up
zmq.notify('Bridge exiting')
zmq.socket.Dispose()
zmq.context.Dispose()

thread.Join()
