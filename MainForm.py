import System.Drawing
import System.Windows.Forms

# from System.Drawing import *
from System import Enum, Byte, Array
from System.Text import Encoding
from System.Windows.Forms import *

from comm import zmq

# fixme: move
keys = {
	Keys.Left: 'Left',
	Keys.Right: 'Right',
	Keys.Up: 'Up',
	Keys.Down: 'Down',
	Keys.End: 'End',
	Keys.Home: 'Home',
	Keys.Delete: 'Delete',
	Keys.Back: 'BackSpace',
	Keys.Tab: 'Tab',
	Keys.PageDown: 'Page_Down',
	Keys.PageUp: 'Page_Up',
	Keys.Space: 'space',
	Keys.OemMinus: 'minus',
	Keys.OemPeriod: '.',
	Keys.OemQuestion: '/',
	Keys.Oemcomma: ',',
	Keys.Oemplus: '=',
	Keys.OemOpenBrackets: '[',
	Keys.Oemtilde: '~',
	Keys.D0: '0',
	Keys.D1: '1',
	Keys.D2: '2',
	Keys.D3: '3',
	Keys.D4: '4',
	Keys.D5: '5',
	Keys.D6: '6',
	Keys.D7: '7',
	Keys.D8: '8',
	Keys.D9: '9',
	Keys.D0: '0',
	Keys.F1: 'F1',
	Keys.F2: 'F2',
	Keys.F3: 'F3',
	Keys.F4: 'F4',
	Keys.F5: 'F5',
	Keys.F6: 'F6',
	Keys.F7: 'F7',
	Keys.F8: 'F8',
	Keys.F9: 'F9',
	Keys.F10: 'F10',
	Keys.F11: 'F11',
	Keys.F12: 'F12',
	Keys.Oem1: ';',
	Keys.Oem5: '|',
	Keys.Oem6: ']',
	Keys.Oem7: '\'',
}


class VoiceTextBox(System.Windows.Forms.RichTextBox):
	pass


class MainForm(Form):
	def __init__(self):
		self.previous_position = 0
		self.handling_keypress = False
		self.InitializeComponent()

	def InitializeComponent(self):
		self._menuStrip1 = System.Windows.Forms.MenuStrip()
		self._statusStrip1 = System.Windows.Forms.StatusStrip()
		self._fileToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._exitToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._textbox = System.Windows.Forms.RichTextBox()
		self._status = System.Windows.Forms.ToolStripStatusLabel()
		self._menuStrip1.SuspendLayout()
		self._statusStrip1.SuspendLayout()
		self.SuspendLayout()
		#
		# menuStrip1
		#
		self._menuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._fileToolStripMenuItem]))
		self._menuStrip1.Location = System.Drawing.Point(0, 0)
		self._menuStrip1.Name = "menuStrip1"
		self._menuStrip1.Size = System.Drawing.Size(284, 24)
		self._menuStrip1.TabIndex = 0
		self._menuStrip1.Text = "menuStrip1"
		#
		# statusStrip1
		#
		self._statusStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._status]))
		self._statusStrip1.Location = System.Drawing.Point(0, 240)
		self._statusStrip1.Name = "statusStrip1"
		self._statusStrip1.Size = System.Drawing.Size(284, 22)
		self._statusStrip1.TabIndex = 1
		#
		# fileToolStripMenuItem
		#
		self._fileToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._exitToolStripMenuItem]))
		self._fileToolStripMenuItem.Name = "fileToolStripMenuItem"
		self._fileToolStripMenuItem.Size = System.Drawing.Size(35, 20)
		self._fileToolStripMenuItem.Text = "File"
		#
		# exitToolStripMenuItem
		#
		self._exitToolStripMenuItem.Name = "exitToolStripMenuItem"
		self._exitToolStripMenuItem.Size = System.Drawing.Size(103, 22)
		self._exitToolStripMenuItem.Text = "Exit"
		#
		# textbox
		#
		self._textbox.AcceptsTab = True
		self._textbox.BorderStyle = System.Windows.Forms.BorderStyle.None
		self._textbox.Dock = System.Windows.Forms.DockStyle.Fill
		self._textbox.HideSelection = False
		self._textbox.ImeMode = System.Windows.Forms.ImeMode.Off
		self._textbox.Location = System.Drawing.Point(0, 24)
		self._textbox.Name = "textbox"
		self._textbox.ShortcutsEnabled = False
		self._textbox.Size = System.Drawing.Size(284, 216)
		self._textbox.TabIndex = 0
		self._textbox.Text = ""
		self._textbox.TextChanged += self.TextboxTextChanged
		self._textbox.KeyDown += self.TextboxKeyDown
		self._textbox.KeyPress += self.TextboxKeyPress
		self._textbox.KeyUp += self.TextboxKeyUp
		self._textbox.PreviewKeyDown += self.TextboxPreviewKeyDown
		#
		# status
		#
		self._status.Name = "status"
		self._status.Size = System.Drawing.Size(0, 17)
		#
		# MainForm
		#
		self.ClientSize = System.Drawing.Size(284, 262)
		self.Controls.Add(self._textbox)
		self.Controls.Add(self._statusStrip1)
		self.Controls.Add(self._menuStrip1)
		self.MainMenuStrip = self._menuStrip1
		self.Name = "MainForm"
		self.Text = "IPYZMQ"
		self._menuStrip1.ResumeLayout(False)
		self._menuStrip1.PerformLayout()
		self._statusStrip1.ResumeLayout(False)
		self._statusStrip1.PerformLayout()
		self.ResumeLayout(False)
		self.PerformLayout()

	def TextboxTextChanged(self, sender, e):
		if self.handling_keypress:
			print '(suppressed: text changed)'
			return

		print 'text changed'
		start_position = self.previous_position
		index = sender.SelectionStart + sender.SelectionLength

		if index < start_position:
			print 'LESS TEXT!', self.previous_position, index
			for _ in range(start_position-index):
				zmq.send_command('BackSpace')
		else:
			text = sender.Text

			print self.previous_position, index

	#		print sender.Text[index]
	#		print self.prevous_position#, index
			print text[start_position:index]
	#		print type(sender.Text)
			zmq.send_key(text[start_position:index])

		self.previous_position = index

	def TextboxKeyPress(self, sender, e):
#		print sender.SelectionStart, sender.SelectionLength
#		print e.KeyChar
#		index = sender.SelectionStart + sender.SelectionLength
#
#		print sender.Text[index]

#		zmq.send_key(e.KeyChar)
		print 'key press'

	def TextboxKeyUp(self, sender, e):
		print 'key up'
		index = sender.SelectionStart + sender.SelectionLength
		# print 'key up, new index:', index
		self.previous_position = index
		self.handling_keypress = False
#
#		print sender.Text[index]
#		zmq.send_key(sender.Text[index])

	def TextboxPreviewKeyDown(self, sender, e):
		ctrl, alt, shift = [(Control.ModifierKeys & modifier) == modifier
							for modifier in (Keys.Control, Keys.Alt, Keys.Shift)]
		modifiers = filter(bool, [ctrl and 'Ctrl', alt and 'Alt', shift and 'Shift'])
		self._status.Text = '+'.join(modifiers + [str(e.KeyCode)])

		modifiers = [e.Control and 'c', e.Alt and 'a', e.Shift and 's']#,
					 #e.Win and 'w']
		modifiers = ''.join(filter(bool, modifiers))

		prefix = modifiers and modifiers + '-' or ''

		if e.KeyCode in keys:
			key = keys[e.KeyCode]
		elif e.KeyCode in (Keys.ControlKey, Keys.ShiftKey):
			key = None
		else:
			key = str(e.KeyCode)

		if key:
			self.handling_keypress = True
			zmq.send_command(prefix + key)

#			e.IsInputKey = True

	def TextboxKeyDown(self, sender, e):
		print 'key down'
#		print e.Alt
		if e.Alt:
			e.SuppressKeyPress = True

	def intercepted_key(self, e):
		# FIXME: Split out of this program
		# FIXME: abstract this
		# should always be a modifier
		modifier, keyname = e.Key.split('-', 1)

		# http://www.codeproject.com/Articles/6768/Tips-about-NET-Enums
		key = Enum.Parse(Keys, keyname)

		if key in keys:
			key = keys[key]

		key = '-'.join((modifier, str(key)))

		print 'intercepted key! ' + key
		zmq.send_command(key)

	def control_thread(self):
		COMMAND_CLEAR = '\x1a'
		COMMAND_TEXT = '\x02'

		socket = zmq.context.Socket(zmq.SocketType.SUB)
		socket.Subscribe(Array[Byte]([0x12]))
		socket.Connect('tcp://vmhost:5556')

		try:
			while True:
				message = socket.Recv(Encoding.UTF8)[1:]

				if not message:
					continue

				command = message[0]

				if command == COMMAND_TEXT:
					message = message[1:]
					print 'set text buffer:', message
				else:
					print 'clear text buffer'
					message = ''

				self.previous_position = 0
				self._textbox.Text = message
				self.previous_position = len(message)
				self._textbox.SelectionLength = 0
				self._textbox.SelectionStart = self.previous_position
		except:
			socket.Dispose()
