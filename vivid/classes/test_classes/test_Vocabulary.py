"""Vocabulary unit tests."""

import pytest
from vivid.classes.vocabulary import Vocabulary
from vivid.classes.relation_symbol import RelationSymbol


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

    # test bad types
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

    # test C and V overlap
    test_ValueError(['O'], [], ['O'])

    C = ['C']
    R = [RelationSymbol('R', 1)]
    R_bad = [RelationSymbol('R', 1), RelationSymbol('R', 1)]
    V = ['V']
    vocab = Vocabulary(C, R, V)
    assert vocab._C is not C
    assert vocab._R is not R
    assert vocab._V is not V

    test_ValueError(C, R_bad, V)


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


def test___contains__():
    """Test in operator for Vocabulary."""
    C = ['C']
    R = [RelationSymbol('R', 1)]
    V = ['V']
    vocabulary = Vocabulary(C, R, V)

    assert 'C' in vocabulary
    assert RelationSymbol('R', 1) in vocabulary
    assert 'V' in vocabulary


def test_add_constant():
    """Test add_constant() function for Vocabulary object."""
    def test_TypeError(vocabulary, c):
        """Test TypeErrors in add_constant."""
        with pytest.raises(TypeError) as excinfo:
            vocabulary.add_constant(c)

    def test_ValueError(vocabulary, c):
        """Test ValueErrors in add constant."""
        with pytest.raises(ValueError) as excinfo:
            vocabulary.add_constant(c)

    C, R, V = ['C'], [RelationSymbol('R', 1)], ['V']
    vocab = Vocabulary(C, R, V)

    test_TypeError(vocab, None)
    test_TypeError(vocab, object)
    test_ValueError(vocab, 'C')
    test_ValueError(vocab, 'V')
    vocab.add_constant('x')
    assert vocab._C == ['C', 'x']
    vocab.add_constant('a')
    assert vocab._C == ['a', 'C', 'x']


def test_add_variable():
    """Test add_variable() function for Vocabulary object."""
    def test_TypeError(vocabulary, v):
        """Test TypeErrors in add_constant."""
        with pytest.raises(TypeError) as excinfo:
            vocabulary.add_variable(v)

    def test_ValueError(vocabulary, v):
        """Test ValueErrors in add constant."""
        with pytest.raises(ValueError) as excinfo:
            vocabulary.add_variable(v)

    C, R, V = ['C'], [RelationSymbol('R', 1)], ['V']
    vocab = Vocabulary(C, R, V)

    test_TypeError(vocab, None)
    test_TypeError(vocab, object)
    test_ValueError(vocab, 'C')
    test_ValueError(vocab, 'V')
    vocab.add_variable('x')
    assert vocab._V == ['V', 'x']
    vocab.add_variable('a')
    assert vocab._V == ['a', 'V', 'x']


def test__key():
    """Test key for hash function."""
    C, R, V = ['C'], [RelationSymbol('R', 1)], ['V']
    vocabulary = Vocabulary(C, R, V)
    assert (('C',), (RelationSymbol('R', 1),), ('V',)) == vocabulary._key()


def test___hash__():
    """Test hash(Vocabulary)."""
    C, R, V = ['C1', 'C2'], [RelationSymbol('R', 1)], ['V']
    vocabulary = Vocabulary(C, R, V)
    C, R, V = ['C2', 'C1'], [RelationSymbol('R', 1)], ['V']
    vocabulary2 = Vocabulary(C, R, V)

    assert hash(vocabulary) == hash(vocabulary2)


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


def test_memory_binding():
    """Test that a vocabulary is shared across all objects that use it."""
    from vivid.classes.attribute import Attribute
    from vivid.classes.relation import Relation
    from vivid.classes.attribute_structure import AttributeStructure
    from vivid.classes.attribute_system import AttributeSystem
    from vivid.classes.constant_assignment import ConstantAssignment
    from vivid.classes.variable_assignment import VariableAssignment
    from vivid.classes.named_state import NamedState
    from vivid.classes.formula import Formula
    from vivid.classes.assumption_base import AssumptionBase
    from vivid.classes.attribute_interpretation import AttributeInterpretation
    from vivid.classes.context import Context

    color = Attribute("color", ['R', 'G', 'B'])
    size = Attribute("size", ['S', 'M', 'L'])
    r = Relation('R1(c) <=> c', ['color'], 1)
    attribute_structure = AttributeStructure(color, size, r)
    o = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, o)

    dummy_rs = RelationSymbol('DUMMY', 3)
    vocabulary = Vocabulary(["dummy"], [dummy_rs], [])
    p = ConstantAssignment(vocabulary, attribute_system, {})
    p2 = ConstantAssignment(vocabulary, attribute_system, {})
    X = VariableAssignment(vocabulary, attribute_system, {})

    s = NamedState(attribute_system, p)
    s2 = NamedState(attribute_system, p2)

    f = Formula(vocabulary, 'DUMMY', "dummy")
    assumption_base = AssumptionBase(f)

    context = Context(assumption_base, s)

    profiles = [[dummy_rs, ('color', 1)]]

    mapping = {dummy_rs: 1}

    attribute_interpretation = AttributeInterpretation(
        vocabulary, attribute_structure, mapping, profiles)

    vocabulary.add_constant("Vocabulary")
    p._vocabulary.add_constant("constant")
    X._vocabulary.add_variable("variable")
    s._p._vocabulary.add_constant("named_state")
    f._vocabulary.add_constant("formula")
    assumption_base._vocabulary.add_constant("assumption_base")
    context._named_state._p._vocabulary.add_constant("context")
    attribute_interpretation._vocabulary.add_constant(
        "attribute_interpretation")

    assert str(vocabulary) == str(p._vocabulary) == str(X._vocabulary) == \
        str(s._p._vocabulary) == str(f._vocabulary) == \
        str(assumption_base._vocabulary) == \
        str(context._named_state._p._vocabulary) == \
        str(attribute_interpretation._vocabulary)

    assert vocabulary is p._vocabulary
    assert vocabulary is X._vocabulary
    assert vocabulary is s._p._vocabulary
    assert vocabulary is f._vocabulary
    assert vocabulary is assumption_base._vocabulary
    assert vocabulary is context._named_state._p._vocabulary
    assert vocabulary is attribute_interpretation._vocabulary
