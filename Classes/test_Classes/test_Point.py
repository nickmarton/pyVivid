"""Point unit tests."""

import pytest
from vivid.Classes.Point import Point

def test___init__():
    """Test Point constructor."""
    def test_TypeError(*dimension_values):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            Point(*dimension_values)
    def test_ValueError(*dimension_values):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            Point(*dimension_values)
    pass

def test___eq__():
    """Test ."""
    pass

def test___ne__():
    """Test ."""
    pass

def test___deepcopy__():
    """Test ."""
    pass

def test__key():
    """Test ."""
    pass

def test___hash__():
    """Test ."""
    pass

def test___str__():
    """Test ."""
    pass

def test___repr__():
    """Test 
    pass.
"""