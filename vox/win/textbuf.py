# coding: utf-8

from difflib import SequenceMatcher


def prune_dictation_context(a, b, insert_point):
    """When inserting before some text, prefer inserting before a matching
    suffix.

    When inserting new text before some existing text, the SequenceMatcher
    wants to preserve any matching suffix on the left of the resulting edits.
    Suppose the existing text is 'it', the insertion point is at the beginning
    of the string, and the new text is 'itinerary it'. The SequenceMatcher will
    produce an insertion at position 2:

        it[inerary it]

    While the text here is correct, this makes keeping track of our insertion
    point much harder (for this particular example, the new insertion point
    is after the space). This function forces the SequenceMatcher to produce a
    left-anchored insertion:

        [itinerary ]it


    """
    # prune matching context before the insertion point
    insert_prefix = first_mismatch(a, b, insert_point)
    if insert_prefix:
        a = a[insert_prefix:]
        b = b[insert_prefix:]
        insert_point -= insert_prefix

    # prune coincidental character matches between the text after the insertion
    # point and the incoming text
    insert_suffix = first_mismatch(a[insert_point:], b[insert_point:])
    if insert_suffix:
        a = a[:-insert_suffix]
        b = b[:-insert_suffix]

    return a, b, insert_point


def generate_edit_keys(a, b, position=None):
    if position is None:
        position = len(a)

    a, b, position = prune_dictation_context(a, b, position)

    length = 0
    edits = []

    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b).get_opcodes():
        if tag == 'equal':
            continue

        if not edits and i1 < position:
            edits.append(('key', 'Left', position - i1))

        if tag in {'delete', 'replace'}:
            edits.append(('key', 'Delete', i2 - i1))
            length -= i2 - i1

        if tag in {'insert', 'replace'}:
            edits.append(b[j1:j2])
            length += j2 - j1

    return edits, length


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

            if not text:
                text = ''
                diff = ('key', 'BackSpace', 1)
                length = 0

            new_text = self._replace_selection(text)
            return Text(new_text, position=self.position + length), [diff]
        else:
            edits, length = generate_edit_keys(self.text, text, self.position)
            position = self.position + length
            return Text(text, position=position), edits

    def __repr__(self):
        return u'<{text}, [{position}:{length}]->"{selected_text}">'.format(
            text=self.text,
            position=self.position,
            length=self.selection_length,
            selected_text=self.selection,
        )


def first_mismatch(a, b, limit=None):
    """Find the index of the first differing element between two sequences."""

    if limit == 0:
        return limit

    enumerator = xrange(max(len(a), len(b)))

    for i, _a, _b in zip(enumerator, a, b):
        if _a != _b or (limit and i >= limit):
            return i
    else:
        return min(len(a), len(b))
