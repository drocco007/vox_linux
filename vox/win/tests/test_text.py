from ..textbuf import Text


def test_initially_empty():
    assert not Text().text


def test_can_initialize_text():
    text = 'Playing again'
    buf = Text(text)

    assert buf.text == text
    assert buf.position == len(text)


def test_can_set_text():
    text = 'Playing'
    new_text = 'Playing again'

    buf = Text(text)
    buf, delta = buf.set_text(new_text)

    result = ' again'

    assert buf.position == len(new_text)
    assert buf.text == new_text
    assert result == delta[0]


def test_set_selection_generates_backward_actions():
    buf = Text('Going backward')
    buf, delta = buf.set_selection(6, 0)

    action, key, count = delta[0]

    assert 'key' == action
    assert 'Left' == key
    assert 8 == count


def test_set_selection_generates_forward_action():
    buf = Text('Moving ahead', position=0)
    buf, delta = buf.set_selection(7, 0)

    action, key, count = delta[0]

    assert 'key' == action
    assert 'Right' == key
    assert 7 == count


def test_set_selection_generates_forward_actions():
    buf = Text('select ME!', position=0)
    buf, delta = buf.set_selection(7, 3)

    assert ('key', 'Right', 7) == delta[0]
    assert ('key', 's-Right', 3) == delta[1]

def test_set_text_can_remove_from_end():
    buf = Text('going away')
    buf, delta = buf.set_text('going')

    assert 'going' == buf.text
    assert len('going') == buf.position

    assert ('key', 'Left', 5) == delta[0]
    assert ('key', 'Delete', 5) == delta[1]


def test_set_text_can_remove_from_middle():
    buf = Text('Playing the game')
    target = 'Playing a gam'
    buf, delta = buf.set_text(target)

    assert target == buf.text
    assert len(target) == buf.position

    assert ('key', 'Left', 8) == delta[0]
    assert ('key', 'Delete', 3) == delta[1]
    assert 'a' == delta[2]


def test_set_text_can_update():
    buf = Text('Playing the game')
    target = 'Playing the Game'
    buf, delta = buf.set_text(target)

    assert target == buf.text
    assert len(target) == buf.position

    assert ('key', 'Left', 4) == delta[0]
    assert ('key', 'Delete', 1) == delta[1]
    assert 'G' == delta[2]


def test_can_shrink_selection():
    buf = Text('Playing the game', position=8, length=4)

    assert 'the ' == buf.selection

    buf, delta = buf.set_selection(8, 3)

    assert 'the' == buf.selection
    assert ('key', 's-Left', 1) == delta[0]


def test_can_expand_selection():
    buf = Text('Play the game', position=5, length=3)

    buf, delta = buf.set_selection(4, 5)

    assert ' the ' == buf.selection

    assert ('key', 'Left', 1) == delta[0]
    assert ('key', 'Left', 1) == delta[1]
    assert ('key', 's-Right', 5) == delta[2]


def test_identical_selection_should_have_no_delta():
    buf = Text('Notebook')
    buf, delta = buf.set_selection(8, 0)
    assert not delta

def test_selected_update():
    buf = Text('Notebook', 0, 8)
    text = 'Netbook'
    buf, delta = buf.set_text(text)

    assert text == delta[0]


def test_can_clear_selection():
    buf = Text('Notebook', 0, 8)
    text = ''
    buf, delta = buf.set_text(text)

    assert ('key', 'BackSpace', 1) == delta[0]


def test_can_clear_interior_selection():
    buf = Text('Notebook', 2, 4)
    text = ''
    buf, delta = buf.set_text(text)

    assert buf.text == 'Nook'
    assert buf.position == 2
    assert buf.selection_length == 0

    assert ('key', 'BackSpace', 1) == delta[0]


def test_can_replace_interior_selection():
    buf = Text('Netbook', 1, 2)
    text = 'Notebook'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 4
    assert buf.selection_length == 0

    assert 'ote' == delta[0]


def test_correct_selection_on_initial_insert():
    buf = Text('Netbook',  0, 0)
    text = 'Notebooks of Netbook'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 13
    assert buf.selection_length == 0


def test_scratch_selection():
    buf = Text('Notebooks of Netbooks',  0, 13)
    text = 'Netbooks'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 0
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert ('key', 'BackSpace', 1) == delta[0]


def test_insert_before_suffix_match():
    """Difficult edge case where initial characters would sometimes be inserted
    after the dictated word preceded by a space:

    Existing: ^it
    Dictate: itinerary
    Expected: itinerary ^it

    Prior to the fix, this scenario would produce "inerary itit"

    """

    buf = Text('it',  0)
    text = 'itinerary it'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 10
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert 'itinerary ' == delta[0]


def test_insert_before_suffix_match2():
    """

    Existing: works ^it
    Dictate: in practice
    Expected: works in practice ^it
    Failure: works n practice i^it

    """

    buf = Text('works it',  6)
    text = 'works in practice it'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 18
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert 'in practice ' == delta[0]


def test_insert_before_suffix_mismatch():
    buf = Text('match',  0)
    text = "doesn't match"
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 8
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert "doesn't " == delta[0]


def test_insert_after_common_prefix():
    """

    Existing: Returns^ a subset
    Dictate: a set
    Expected: Returns a set^ a subset
    Failure case: Returnset a s^ a subset

    """

    buf = Text('Returns a subset',  7)
    text = 'Returns a set a subset'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 13
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert ' a set' == delta[0]


def test_insert_after_common_prefix_space():
    """

    Existing: Returns ^a subset
    Dictate: a set
    Expected: Returns a set ^a subset
    Failure case: Returns et a s^a subset

    """

    buf = Text('Returns a subset',  8)
    text = 'Returns a set a subset'
    buf, delta = buf.set_text(text)

    assert buf.text == text
    assert buf.position == 14
    assert buf.selection_length == 0

    assert 1 == len(delta)
    assert 'a set ' == delta[0]
