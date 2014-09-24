from time import time
import sys

import System.Drawing
import System.Windows.Forms

# from System.Drawing import *
from System import Enum, Byte, Array
from System.Text import Encoding
from System.Windows.Forms import *

import clr
clr.AddReference('IronPython')
from IronPython.Compiler import CallTarget0

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


import logging as log

class VoiceTextBox(System.Windows.Forms.RichTextBox):
    pass


class MainForm(Form):
    def __init__(self):
        self.previous_position = 0
        self.handling_keypress = False
        self.processing_dictation = False
        self.InitializeComponent()

    def InitializeComponent(self):
        self._statusStrip1 = System.Windows.Forms.StatusStrip()
        self._textbox = System.Windows.Forms.RichTextBox()
        self._status = System.Windows.Forms.ToolStripStatusLabel()
        self._statusStrip1.SuspendLayout()
        self.SuspendLayout()
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
        # self._textbox.KeyDown += self.TextboxKeyDown
        # self._textbox.KeyPress += self.TextboxKeyPress
        self._textbox.KeyUp += self.TextboxKeyUp
        self._textbox.PreviewKeyDown += self.TextboxPreviewKeyDown


        print
        print 'Textbox handle:', self._textbox.Handle
        print

        # import win32com
        # self.de = win32com.client.Dispatch('Dragon.DictEdit.1')
        #
        # http://stackoverflow.com/a/3518253
        from System import Type, Activator
        self.de = Activator.CreateInstance(Type.GetTypeFromProgID('Dragon.DictEdit.1'))
        # self.de = Activator.CreateInstance(Type.GetTypeFromProgID('Dragon.DictCustom.1'))

        # print
        # print self.de.Enabled
        self.de.Register(self._textbox.Handle, 1)
        self.de.hWndActivate = None
        self.de.TextChanged += self.handle_de_text_changed

        # self.de.Register()
        # self.de.hWndActivate = self.Handle
        # self.Active = True

        # print dir(self.de)
        # print self.de.Enabled
        # print self.de.hwndEdit
        # print self.de.hwndActivate
        # print

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
        self.Name = "MainForm"
        self.Text = "IPYZMQ"
        self._statusStrip1.ResumeLayout(False)
        self._statusStrip1.PerformLayout()
        self.ResumeLayout(False)
        self.PerformLayout()

    def TextboxTextChanged(self, sender, e):
        if self.handling_keypress:
            log.info('(suppressed: text changed)')
            return True
        # if not self.processing_dictation:
        #     log.info('(suppressed: no dictation; current text: %s)', self._textbox.Text)
        #     return

        log.info('text changed')
        start_position = self.previous_position
        index = sender.SelectionStart + sender.SelectionLength

        if index < start_position:
            log.info('LESS TEXT! %d %d', self.previous_position, index)

            # FIXME
            for _ in range(start_position-index):
                zmq.send_command('BackSpace')
        else:
            text = sender.Text

            # log.info('%d %d', self.previous_position, index)

    #       log.info(sender.Text[index])
    #       log.info(self.prevous_position#, index)
            log.info(text[start_position:index])
    #       log.info(type(sender.Text))
            zmq.send_key(text[start_position:index])

        self.previous_position = index
        self.processing_dictation = False

        return True

#     def TextboxKeyPress(self, sender, e):
# #       log.info(sender.SelectionStart, sender.SelectionLength)
# #       log.info(e.KeyChar)
# #       index = sender.SelectionStart + sender.SelectionLength
# #
# #       log.info(sender.Text[index])

# #       zmq.send_key(e.KeyChar)
#         log.info('key press')

    def TextboxKeyUp(self, sender, e):
        log.info('key up')
        index = sender.SelectionStart + sender.SelectionLength
        # log.info('key up, new index:', index)
        self.previous_position = index
        self.handling_keypress = False
        return True
#
#       log.info(sender.Text[index])
#       zmq.send_key(sender.Text[index])

    def TextboxPreviewKeyDown(self, sender, e):
        log.info('preview key down')

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

#           e.IsInputKey = True
        return True

#     def TextboxKeyDown(self, sender, e):
#         log.info('key down')
# #       log.info(e.Alt)
#         if e.Alt:
#             e.SuppressKeyPress = True

    def handle_de_text_changed(self, *args, **kw):
        log.info('handle_de_text_changed: %s, %s', args, kw)
        self.processing_dictation = True
        return True

    def intercepted_key(self, e):
        log.info('intercepted key event')
        # FIXME: Split out of this program
        # FIXME: abstract this
        # should always be a modifier
        modifier, keyname = e.Key.split('-', 1)

        # http://www.codeproject.com/Articles/6768/Tips-about-NET-Enums
        key = Enum.Parse(Keys, keyname)

        if key in keys:
            key = keys[key]

        key = '-'.join((modifier, str(key)))

        log.info('intercepted key: ' + key)
        zmq.send_command(key)

    def set_text(self, text='', cursor_position=None):
        self.handling_keypress = True

        if cursor_position is None:
            cursor_position = len(text)

        # self._menuStrip1.Focus()
        # self.de.Reset()
        self.previous_position = cursor_position
        self._textbox.Modified = True
        self._textbox.Text = text
        # self._textbox.Clear()

        # if text:
        #   self._textbox.AppendText(text)

        self._textbox.SelectionLength = 0
        self._textbox.SelectionStart = self.previous_position
        # self._textbox.AppendText('')
        # log.info('\n\n\n%s %d %d\n\n\n', self._textbox.Text, self._textbox.SelectionStart, self._textbox.SelectionLength)
        self.handling_keypress = False
        # self._textbox.Focus()

    def control_thread(self):
        log.info('starting control_thread')

        COMMAND_CLEAR = '\x1a'
        COMMAND_TEXT = '\x02'

        log.info('control_thread started')

        def read_messages():
            message = sys.stdin.readline()

            while message:
                log.debug('raw message: "%s"', message)
                yield message
                message = sys.stdin.readline()

        for message in read_messages():
            if message[0] != '\x12':
                continue

            log.info('control message: "%s"', message)
            command = message[1]

            if command == COMMAND_TEXT:
                message = message[2:].strip()
                log.info('set text buffer: %s', message)
            else:
                log.info('clear text buffer')
                message = ''

            def _update():
                # self.de.Reset()
                self.set_text(message)
                # self.handling_keypress = False

            self._textbox.BeginInvoke(CallTarget0(_update))

            log.info('control message processing complete')

        log.info('control_thread stopping')