# coding: utf-8

from difflib import SequenceMatcher


def generate_edit_keys(a, b, position=None):
    if position is None:
        position = len(a)

    edits = []

    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b).get_opcodes():
        if tag == 'equal':
            continue

        if not edits and i1 < position:
            edits.append(('key', 'Left', position - i1))

        if tag in {'delete', 'replace'}:
            edits.append(('key', 'Delete', i2 - i1))

        if tag in {'insert', 'replace'}:
            edits.append(b[j1:j2])

    return edits


class Text(object):
    def __init__(self, text='', position=None, length=0):
        self.text = text
        self.position = position if position is not None else len(text)
        self.selection_length = length
        self.selection = text[self.position:self.position + length]

    def _replace_selection(self, text):
        prefix, postfix = self.text[:self.position], \
            self.text[self.position + self.selection_length:]
        return ''.join((prefix, text, postfix))

    def expand_selection(self, position, length):
        delta = length - self.selection_length

        if delta < 0:
            diff = [('key', 's-Left', abs(delta))]
        else:
            diff = [('key', 's-Right', delta)]

        return Text(self.text, position, length), diff

    def set_selection(self, position, length):
        diff = []

        if self.selection_length:
            if self.position == position:
                return self.expand_selection(position, length)
            else:
                diff.append(('key', 'Left', 1))

        delta = self.position - position

        if delta < 0:
            diff.append(('key', 'Right', abs(delta)))
        elif delta > 0:
            diff.append(('key', 'Left', delta))

        if length:
            diff.append(('key', 's-Right', length))

        return Text(self.text, position, length), diff

    def set_text(self, text):
        if self.selection:
            if text:
                i = self.position
                length = self.selection_length + len(text) - len(self.text)
                text = text[i:i + length]
                diff = text
            else:
                text = ''
                diff = ('key', 'BackSpace', 1)

            new_text = self._replace_selection(text)
            return Text(new_text, position=self.position + len(text)), [diff]
        else:
            return Text(text), generate_edit_keys(self.text, text, self.position)

    def __repr__(self):
        return u'<{text}, [{position}:{length}]→"{selected_text}">'.format(
            text=self.text,
            position=self.position,
            length=self.selection_length,
            selected_text=self.selection,
        )