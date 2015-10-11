"""Attribute class unit tests."""

import pytest
from Attribute import Attribute

def test_set_label():
    """Test set label function."""

    def test_labels(label):
        """Test set_label with label param."""
        with pytest.raises(TypeError) as excinfo:
            A.set_label(label)

    A = Attribute("", [])
    
    test_labels(1)
    test_labels(1.0)
    test_labels([])
    test_labels(set([]))
    test_labels(object)

def test_set_possible_values():
    """Test set_possible_values function."""

    def test_labels(value_set):
        with pytest.raises(TypeError) as excinfo:
            A.set_possible_values(value_set)

    A = Attribute("", [])
    
    test_labels(1)
    test_labels(1.0)
    test_labels("")
    test_labels(set([]))
    test_labels(object)

def test_eq():
    """Test __eq__ magic function."""
    A1, A2 = Attribute("label", []), Attribute("label", [])
    assert A1 == A2

def test_ne():
    """Test __ne__ magic function."""
    A1, A2 = Attribute("lbl", []), Attribute("label", [])
    A3, A4 = Attribute("label", [1]), Attribute("label", [])
    assert A1 != A2
    assert A3 != A4
