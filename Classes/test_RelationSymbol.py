"""RelationSymbol unit tests."""

import pytest
from vivid.Classes.RelationSymbol import RelationSymbol

def test___init__():
    """Test RelationSymbol constructor."""
    def test_TypeError(name, arity):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            RelationSymbol(name, arity)

    test_TypeError(1, 1)
    test_TypeError('', '')

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
