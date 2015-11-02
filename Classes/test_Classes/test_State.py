"""State unit tests."""

import pytest
from vivid.Classes.State import State
from vivid.Classes.State import AttributeSystem
from vivid.Classes.State import AttributeStructure
from vivid.Classes.State import Attribute, Relation

def test___init__():
    """Test State constructor."""
    def test_TypeError(attrsys, **asc):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            State(attrsys, **asc)

    def test_ValueError(attrsys, **asc):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            State(attrsys, **asc)

    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    R3 = Relation("R3(a) <=> ", ["a"], 3)
    astr = AttributeStructure()

    #TODO further implementation
    pass

def test___eq__():
    """Test == operator."""
    a = Attribute("a", [])
    b = Attribute("b", [])
    R1 = Relation("R1(a) <=> ", ["a1"], 1)
    R2 = Relation("R2(a) <=> ", ["b"], 2)
    R3 = Relation("R3(a) <=> ", ["a"], 3)
    astr = AttributeStructure()

    pass

def test___lt__():
    """Test < operator overloaded for proper extension."""
    pass

def test___le__():
    """Test <= operator overloaded for extension."""
    pass

def test___ne__():
    """Test != operator."""
    pass

def test___deepcopy__():
    """Test deepcopy"""
    pass

def test_set_ascription():
    """Test set_ascription function."""
    pass

def test___getitem__():
    """Test indexing for State"""
    pass

def test_is_valuation():
    """Test is_valuation function."""
    pass

def test_is_world():
    """Test is_world function."""
    pass

def test_get_worlds():
    """Test get_worlds function."""
    pass

def test_is_alternate_extension():
    """Test is_alternate_extension function."""
    pass

def test_get_alternate_extensions():
    """Test get_alternate_extensions function."""
    pass

def test___str__():
    """Test str(State)"""
    pass

def test___repr__():
    """."""
    pass
