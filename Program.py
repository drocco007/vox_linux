import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

import sys
sys.path.append(r'v:\IPYZMQ\bin\Debug')
clr.AddReferenceToFile('KeyIntercept.dll')

#clr.AddReferenceToFile("KeyIntercept.dll")
from KeyIntercept import KeyboardHook

from System.Windows.Forms import Application
import MainForm


keyboard_hook = KeyboardHook.setHook()

Application.EnableVisualStyles()
form = MainForm.MainForm()

keyboard_hook.KeyIntercepted += form.intercepted_key

Application.Run(form)
