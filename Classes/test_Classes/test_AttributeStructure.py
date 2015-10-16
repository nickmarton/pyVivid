"""Attribute Structure unit tests."""

import pytest
from ..AttributeStructure import AttributeStructure

def test_init():
    """."""

    def test_type_params(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(TypeError) as excinfo:
            pass
    def test_value_params(definition, D_of_r, subscript):
        """Test constructor for TypeErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            pass