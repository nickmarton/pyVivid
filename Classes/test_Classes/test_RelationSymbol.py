"""RelationSymbol unit tests."""

import pytest
from vivid.Classes.RelationSymbol import RelationSymbol


def test___init__():
    """Test RelationSymbol constructor."""
    def test_TypeError(name, arity):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            RelationSymbol(name, arity)

    def test_ValueError(name, arity):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            RelationSymbol(name, arity)

    test_TypeError(1, 1)
    test_TypeError('', '')
    test_ValueError('name', 0)
    test_ValueError('name', -1)


def test___eq__():
    """Test == operator for RelationSymbol."""
    rs1 = RelationSymbol('name1', 1)
    rs2 = RelationSymbol('name1', 1)
    rs3 = RelationSymbol('name1', 2)
    rs4 = RelationSymbol('name2', 1)

    assert rs1 == rs1
    assert rs1 == rs2
    assert not rs1 == rs3
    assert not rs1 == rs4


def test___ne__():
    """Test != operator for RelationSymbol."""
    rs1 = RelationSymbol('name1', 1)
    rs2 = RelationSymbol('name1', 1)
    rs3 = RelationSymbol('name1', 2)
    rs4 = RelationSymbol('name2', 1)

    assert not rs1 != rs1
    assert not rs1 != rs2
    assert rs1 != rs3
    assert rs1 != rs4


def test___deepcopy__():
    """Test copy.deepcopy for RelationSymbol object."""
    from copy import deepcopy
    r = RelationSymbol('name', 1)
    r_copy = deepcopy(r)

    assert r == r_copy
    assert r is not r_copy


def test__key():
    """Test key for RelationSymbol hashing."""
    r = RelationSymbol('name', 1)
    assert r._key() == ('name', 1)


def test___hash__():
    """Test hasing for RelationSymbol."""
    r = RelationSymbol('name', 1)
    assert hash(r) == 1828406127258546681


def test___str__():
    """Test str(RelationSymbol)."""
    rs1 = RelationSymbol('name', 1)
    rs2 = RelationSymbol('', 1)
    assert rs1.__str__() == 'name'
    assert rs2.__str__() == ''


def test___repr__():
    """Test repr(RelationSymbol."""
    rs1 = RelationSymbol('name', 1)
    rs2 = RelationSymbol('', 1)
    assert rs1.__repr__() == 'name'
    assert rs2.__repr__() == ''
