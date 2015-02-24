SHOW_NOTIFICATION = '\x01'
PRESS_KEY = '\x02'
PLAY_TEXT = '\x03'
BROADCAST_APPLICATION_TITLE = '\x05'
RUN_COMMAND = '\x11'
RECORD_SEPARATOR='\x1e'

MANAGE_BUFFER = '\x12'
BUFFER_SET_TEXT = '\x02'
BUFFER_CLEAR = '\x1a'

CLEAR_BUFFER_COMMAND = ''.join((MANAGE_BUFFER, BUFFER_CLEAR))


def is_text_command(message):
    "Determine if a message is a text entry command (press key or play text)"

    return message and message[0] in {PRESS_KEY, PLAY_TEXT}


def format_app_name_command(window_name, application_name):
    "Format application name and title broadcast command"

    return '{}{}{}{}'.format(BROADCAST_APPLICATION_TITLE,
                             window_name,
                             RECORD_SEPARATOR,
                             application_name)
