"""Vocabulary unit tests."""

import pytest
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.RelationSymbol import RelationSymbol

def test___init__():
    """Test Vocabulary constructor."""
    def test_TypeError(C, R, V):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Vocabulary(C, R, V)
    def test_ValueError(C, R, V):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Vocabulary(C, R, V)

    #test bad types
    test_TypeError(None, [], [])
    test_TypeError([], None, [])
    test_TypeError([], [], None)
    test_TypeError(object, [], [])
    test_TypeError([], object, [])
    test_TypeError([], [], object)
    test_TypeError([1], [], [])
    test_TypeError([], [1], [])
    test_TypeError([], [''], [])
    test_TypeError([], [], [1])

    #test C and V overlap
    test_ValueError(['O'], [], ['O'])

    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    assert vocab._C is not C
    assert vocab._R is not R
    assert vocab._V is not V

def test___eq__():
    """Test == operator for Vocabulary."""
    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    vocab_copy = Vocabulary(C, R, V)

    C = ['C\'']
    R = [RelationSymbol('R\'', 1)]
    V = ['V\'']
    vocab_prime = Vocabulary(C, R, V)

    assert vocab == vocab
    assert vocab == vocab_copy
    assert vocab is not vocab_copy
    assert not vocab == vocab_prime    

def test___ne__():
    """Test != operator for Vocabulary."""
    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    vocab_copy = Vocabulary(C, R, V)

    C = ['C\'']
    R = [RelationSymbol('R\'', 1)]
    V = ['V\'']
    vocab_prime = Vocabulary(C, R, V)

    assert not vocab != vocab
    assert not vocab != vocab_copy
    assert vocab is not vocab_copy
    assert vocab != vocab_prime

def test___deepcopy__():
    """Test copy.deepcopy for Vocabulary."""
    from copy import deepcopy

    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    vocab_copy = deepcopy(vocab)

    assert vocab == vocab_copy
    assert vocab is not vocab_copy
    assert vocab._C is not vocab_copy._C
    assert vocab._R is not vocab_copy._R
    assert vocab._V is not vocab_copy._V

def test_constant_assignment():
    """Test constant assignment mapping."""
    pass

def test_variable_assignment():
    """Test Test constant assignment mapping."""
    pass

def test___str__():
    """Test str(Vocabulary)."""
    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    assert vocab.__str__() == "([C], [R], [V])"

    vocab_empty = Vocabulary([], [], [])
    assert vocab_empty.__str__() == "([], [], [])"

def test___repr__():
    """Test repr(Vocabulary)."""
    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    assert vocab.__repr__() == "([C], [R], [V])"

    vocab_empty = Vocabulary([], [], [])
    assert vocab_empty.__repr__() == "([], [], [])"