# coding: utf-8

import uinput
import zmq

from commands import PRESS_KEY, PLAY_TEXT
from process_utils import spawn_daemon_process


UNICODE_PREFIX = [uinput.KEY_RIGHTALT, uinput.KEY_LEFTCTRL,
                  uinput.KEY_LEFTSHIFT, uinput.KEY_U]

modifier_map = {
    'a': uinput.KEY_RIGHTALT,
    'c': uinput.KEY_LEFTCTRL,
    's': uinput.KEY_LEFTSHIFT,
    'w': uinput.KEY_LEFTMETA,
}


key_map = {
    'a': uinput.KEY_A,
    'b': uinput.KEY_B,
    'c': uinput.KEY_C,
    'd': uinput.KEY_D,
    'e': uinput.KEY_E,
    'f': uinput.KEY_F,
    'g': uinput.KEY_G,
    'h': uinput.KEY_H,
    'i': uinput.KEY_I,
    'j': uinput.KEY_J,
    'k': uinput.KEY_K,
    'l': uinput.KEY_L,
    'm': uinput.KEY_M,
    'n': uinput.KEY_N,
    'o': uinput.KEY_O,
    'p': uinput.KEY_P,
    'q': uinput.KEY_Q,
    'r': uinput.KEY_R,
    's': uinput.KEY_S,
    't': uinput.KEY_T,
    'u': uinput.KEY_U,
    'v': uinput.KEY_V,
    'w': uinput.KEY_W,
    'x': uinput.KEY_X,
    'y': uinput.KEY_Y,
    'z': uinput.KEY_Z,
    '1': uinput.KEY_1,
    '2': uinput.KEY_2,
    '3': uinput.KEY_3,
    '4': uinput.KEY_4,
    '5': uinput.KEY_5,
    '6': uinput.KEY_6,
    '7': uinput.KEY_7,
    '8': uinput.KEY_8,
    '9': uinput.KEY_9,
    '0': uinput.KEY_0,

    '\t': uinput.KEY_TAB,
    'Tab': uinput.KEY_TAB,
    '\n': uinput.KEY_ENTER,
    'Return': uinput.KEY_ENTER,
    ' ': uinput.KEY_SPACE,
    'space': uinput.KEY_SPACE,
    'Delete': uinput.KEY_DELETE,
    'Escape': uinput.KEY_ESC,
    'BackSpace': uinput.KEY_BACKSPACE,

    '.': uinput.KEY_DOT,
    ',': uinput.KEY_COMMA,
    '/': uinput.KEY_SLASH,
    '\\': uinput.KEY_BACKSLASH,
    "'": uinput.KEY_APOSTROPHE,
    ';': uinput.KEY_SEMICOLON,
    '[': uinput.KEY_LEFTBRACE,
    ']': uinput.KEY_RIGHTBRACE,
    '-': uinput.KEY_MINUS,
    'minus': uinput.KEY_MINUS,
    '=': uinput.KEY_EQUAL,

    'Left': uinput.KEY_LEFT,
    'Right': uinput.KEY_RIGHT,
    'Up': uinput.KEY_UP,
    'Down': uinput.KEY_DOWN,
    'Home': uinput.KEY_HOME,
    'End': uinput.KEY_END,
    'Page_Up': uinput.KEY_PAGEUP,
    'Page_Down': uinput.KEY_PAGEDOWN,
    'Insert': uinput.KEY_INSERT,

    'F1': uinput.KEY_F1,
    'F2': uinput.KEY_F2,
    'F3': uinput.KEY_F3,
    'F4': uinput.KEY_F4,
    'F5': uinput.KEY_F5,
    'F6': uinput.KEY_F6,
    'F7': uinput.KEY_F7,
    'F8': uinput.KEY_F8,
    'F9': uinput.KEY_F9,
    'F10': uinput.KEY_F10,
    'F11': uinput.KEY_F11,
    'F12': uinput.KEY_F12,
}


chord_map = {
    ':': [uinput.KEY_LEFTSHIFT, uinput.KEY_SEMICOLON],
    '?': [uinput.KEY_LEFTSHIFT, uinput.KEY_SLASH],
    '"': [uinput.KEY_LEFTSHIFT, uinput.KEY_APOSTROPHE],
    '+': [uinput.KEY_LEFTSHIFT, uinput.KEY_EQUAL],
    '_': [uinput.KEY_LEFTSHIFT, uinput.KEY_MINUS],
}


# FIXME: extract to a common module
def init_zmq(host='localhost'):
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://{}:5556'.format(host))

    socket.setsockopt(zmq.SUBSCRIBE, PRESS_KEY)
    socket.setsockopt(zmq.SUBSCRIBE, PLAY_TEXT)

    return socket


def unpack_keycodes(command):
    if '-' in command:
        modifiers, command = command.split('-', 1)
        modifiers = [modifier_map[modifier] for modifier in modifiers]
    else:
        modifiers = []

    return modifiers + [key_map.get(command, command)]


def emit_text(kbd, text):
    """Send a text string to the keyboard.

    Send an arbitrary string of text to the given keyboard.

    * if the character is defined in the chord_map, send the chord directly
    * if the character is an uppercase letter, send the chord consisting of
      the left shift key and the lowercase version of the letter
    * if the character is defined in the key_map, enter it directly
    * otherwise assume it is a Unicode character, which is entered using
      the code point entry method: <cas-u> <4-digit hex code> <space>

    """

    for char in text:
        if char in chord_map:
            kbd.emit_combo(chord_map[char], syn=True)
        elif char.isupper():
            chord = [uinput.KEY_LEFTSHIFT, key_map[char.lower()]]
            kbd.emit_combo(chord, syn=True)
        elif char in key_map:
            kbd.emit_click(key_map[char], syn=True)
        else:
            codepoint = hex(ord(char))[2:] + u' '
            kbd.emit_combo(UNICODE_PREFIX, syn=True)
            emit_text(kbd, codepoint)


def relay_text_worker(host='localhost'):
    socket = init_zmq(host=host)

    all_keys = [uinput.ev.__dict__[k]
                for k in uinput.ev.__dict__.keys() if k.startswith('KEY_')]

    with uinput.Device(all_keys) as kbd:
        while True:
            message = socket.recv()

            command, message = message[0], message[1:]

            try:
                if command == PRESS_KEY:
                    keycodes = unpack_keycodes(message)

                    # print '.key:', message[1:], '→', keycodes
                    kbd.emit_combo(keycodes)
                else:
                    # print '.text: {} ({})'.format(message, type(message))
                    emit_text(kbd, unicode(message))
            except ValueError as e:
                print u'Error processing message: {}'.format(message)


def relay_text(host='localhost'):
    return [spawn_daemon_process(relay_text_worker, call_kw={'host': host})]
