from vox.win.textbuf import first_mismatch

import pytest


def test_zero_length_strings():
    assert 0 == first_mismatch('', '')


def test_should_be_length_of_identical_single_character_strings():
    assert 1 == first_mismatch('a', 'a')


def test_should_be_beginning_of_different_single_character_strings():
    assert 0 == first_mismatch('b', 'c')


@pytest.mark.parametrize('target', ['d', 'de', 'the', 'quad', '     '])
def test_should_be_beginning_with_zero_length_source(target):
    assert 0 == first_mismatch('', target)


@pytest.mark.parametrize('source', ['z', 'ea', 'the', 'quad', '     '])
def test_should_be_beginning_with_zero_length_target(source):
    assert 0 == first_mismatch(source, '')


def test_should_be_length_of_identical_two_character_strings():
    assert 2 == first_mismatch('az', 'az')


def test_should_be_beginning_of_different_two_character_strings():
    assert 0 == first_mismatch('bx', 'cw')


def test_first_mismatch_with_2_character_strings():
    assert 1 == first_mismatch('ab', 'a ')


def test_different_length_strings():
    a = 'Returns a subset'
    b = 'Returns a set a subset'
    assert 11 == first_mismatch(a, b)


def test_different_length_strings_with_limit():
    a = 'Returns a subset'
    b = 'Returns a set a subset'
    assert 7 == first_mismatch(a, b, 7)


def test_different_length_strings_with_limit_past_mismatch():
    a = 'Returns a subset'
    b = 'Returns a set a subset'
    assert 11 == first_mismatch(a, b, 15)
