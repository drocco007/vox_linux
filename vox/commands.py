SHOW_NOTIFICATION = '\x01'
PRESS_KEY = '\x02'
PLAY_TEXT = '\x03'
BROADCAST_APPLICATION_TITLE = '\x05'
RUN_COMMAND = '\x11'
RECORD_SEPARATOR='\x1e'

MANAGE_BUFFER = '\x12'
BUFFER_SET_TEXT = '\x02'
BUFFER_CLEAR = '\x1a'


def is_text_command(message):
    "Determine if a message is a text entry command (press key or play text)"

    return message and message[0] in {PRESS_KEY, PLAY_TEXT}
