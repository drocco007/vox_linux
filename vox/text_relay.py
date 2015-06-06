# coding: utf-8

from evdev import UInput, ecodes

import bus
from commands import PRESS_KEY, PLAY_TEXT
from process_utils import spawn_daemon_process


UNICODE_PREFIX = [ecodes.KEY_RIGHTALT, ecodes.KEY_LEFTCTRL,
                  ecodes.KEY_LEFTSHIFT, ecodes.KEY_U]

modifier_map = {
    'a': ecodes.KEY_RIGHTALT,
    'c': ecodes.KEY_LEFTCTRL,
    's': ecodes.KEY_LEFTSHIFT,
    'w': ecodes.KEY_LEFTMETA,
}


key_map = {
    'a': ecodes.KEY_A,
    'b': ecodes.KEY_B,
    'c': ecodes.KEY_C,
    'd': ecodes.KEY_D,
    'e': ecodes.KEY_E,
    'f': ecodes.KEY_F,
    'g': ecodes.KEY_G,
    'h': ecodes.KEY_H,
    'i': ecodes.KEY_I,
    'j': ecodes.KEY_J,
    'k': ecodes.KEY_K,
    'l': ecodes.KEY_L,
    'm': ecodes.KEY_M,
    'n': ecodes.KEY_N,
    'o': ecodes.KEY_O,
    'p': ecodes.KEY_P,
    'q': ecodes.KEY_Q,
    'r': ecodes.KEY_R,
    's': ecodes.KEY_S,
    't': ecodes.KEY_T,
    'u': ecodes.KEY_U,
    'v': ecodes.KEY_V,
    'w': ecodes.KEY_W,
    'x': ecodes.KEY_X,
    'y': ecodes.KEY_Y,
    'z': ecodes.KEY_Z,
    '1': ecodes.KEY_1,
    '2': ecodes.KEY_2,
    '3': ecodes.KEY_3,
    '4': ecodes.KEY_4,
    '5': ecodes.KEY_5,
    '6': ecodes.KEY_6,
    '7': ecodes.KEY_7,
    '8': ecodes.KEY_8,
    '9': ecodes.KEY_9,
    '0': ecodes.KEY_0,

    '\t': ecodes.KEY_TAB,
    'Tab': ecodes.KEY_TAB,
    '\n': ecodes.KEY_ENTER,
    'Return': ecodes.KEY_ENTER,
    ' ': ecodes.KEY_SPACE,
    'space': ecodes.KEY_SPACE,
    'Delete': ecodes.KEY_DELETE,
    'Escape': ecodes.KEY_ESC,
    'BackSpace': ecodes.KEY_BACKSPACE,

    '.': ecodes.KEY_DOT,
    ',': ecodes.KEY_COMMA,
    '/': ecodes.KEY_SLASH,
    '\\': ecodes.KEY_BACKSLASH,
    "'": ecodes.KEY_APOSTROPHE,
    ';': ecodes.KEY_SEMICOLON,
    '[': ecodes.KEY_LEFTBRACE,
    ']': ecodes.KEY_RIGHTBRACE,
    '-': ecodes.KEY_MINUS,
    'minus': ecodes.KEY_MINUS,
    '=': ecodes.KEY_EQUAL,
    '~': ecodes.KEY_GRAVE,

    'Left': ecodes.KEY_LEFT,
    'Right': ecodes.KEY_RIGHT,
    'Up': ecodes.KEY_UP,
    'Down': ecodes.KEY_DOWN,
    'Home': ecodes.KEY_HOME,
    'End': ecodes.KEY_END,
    'Page_Up': ecodes.KEY_PAGEUP,
    'Page_Down': ecodes.KEY_PAGEDOWN,
    'Insert': ecodes.KEY_INSERT,

    'F1': ecodes.KEY_F1,
    'F2': ecodes.KEY_F2,
    'F3': ecodes.KEY_F3,
    'F4': ecodes.KEY_F4,
    'F5': ecodes.KEY_F5,
    'F6': ecodes.KEY_F6,
    'F7': ecodes.KEY_F7,
    'F8': ecodes.KEY_F8,
    'F9': ecodes.KEY_F9,
    'F10': ecodes.KEY_F10,
    'F11': ecodes.KEY_F11,
    'F12': ecodes.KEY_F12,
}


chord_map = {
    ':': [ecodes.KEY_LEFTSHIFT, ecodes.KEY_SEMICOLON],
    '?': [ecodes.KEY_LEFTSHIFT, ecodes.KEY_SLASH],
    '"': [ecodes.KEY_LEFTSHIFT, ecodes.KEY_APOSTROPHE],
    '+': [ecodes.KEY_LEFTSHIFT, ecodes.KEY_EQUAL],
    '_': [ecodes.KEY_LEFTSHIFT, ecodes.KEY_MINUS],
}


def unpack_keycodes(command):
    if '-' in command:
        modifiers, command = command.split('-', 1)
        modifiers = [modifier_map[modifier] for modifier in modifiers]
    else:
        modifiers = []

    return modifiers + [key_map.get(command, command)]


def emit_combo(kbd, keys, syn=False):
    for key in keys:
        kbd.write(ecodes.EV_KEY, key, 1)

    for key in reversed(keys):
        kbd.write(ecodes.EV_KEY, key, 0)

    if syn:
        kbd.syn()


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
            emit_combo(kbd, chord_map[char], syn=True)
        elif char.isupper():
            chord = [ecodes.KEY_LEFTSHIFT, key_map[char.lower()]]
            emit_combo(kbd, chord, syn=True)
        elif char in key_map:
            emit_combo(kbd, [key_map[char]], syn=True)
        else:
            codepoint = hex(ord(char))[2:] + u' '
            emit_combo(kbd, UNICODE_PREFIX, syn=True)
            emit_text(kbd, codepoint)


def relay_text_worker(host='localhost'):
    socket = bus.connect_subscribe(host=host,
                                   subscriptions=(PRESS_KEY, PLAY_TEXT))

    # all_keys = [v for k,v in uinput.ev.__dict__.items()
                # if k.startswith('KEY_')]

    with UInput() as kbd:
        while True:
            message = socket.recv()

            command, message = message[0], message[1:]

            try:
                if command == PRESS_KEY:
                    keycodes = unpack_keycodes(message)

                    print '.key:', message, '→', keycodes
                    emit_combo(kbd, keycodes)
                else:
                    print '.text: {} ({})'.format(message, type(message))
                    emit_text(kbd, unicode(message))
            except ValueError as e:
                print u'Error processing message: {}'.format(message)

            kbd.syn()


def relay_text(host='localhost'):
    return [spawn_daemon_process(relay_text_worker, call_kw={'host': host})]
