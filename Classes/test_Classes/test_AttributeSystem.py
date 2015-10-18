"""Attribute System unit tests."""

import pytest
from ..AttributeSystem import AttributeSystem
from ..AttributeSystem import AttributeStructure
from ..AttributeSystem import Attribute, Relation

def test___init__():
    """."""
    def test_TypeError(A, objs):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            AttributeSystem(A, objs)

    def test_ValueError(A, objs):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            AttributeSystem(A, objs)


def test___eq__():
    """."""
    pass

def test___le__():
    """."""
    pass

def test___ne__():
    """."""
    pass

def test___add__():
    """."""
    pass

def test___sub__():
    """."""
    pass

def test___iadd__():
    """."""
    pass

def test___isub__():
    """."""
    pass

def test___getitem__():
    """."""
    pass

def test___contains__():
    """."""
    pass

def test___deepcopy__():
    """."""
    pass

def test_get_power():
    """."""
    pass

def test___str__():
    """."""
    pass

def test___repr__():
    """."""
    pass

def test_is_automorphic():
    """."""
    pass
