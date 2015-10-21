"""ValueSet class unit tests."""

import pytest
from vivid.Classes.ValueSet import ValueSet

def test_add_object_type():
    """."""
    pass

def test___init__():
    """Test ValueSet Constructor"""
    def test_TypeError(valueset):
        """Test an individual ValueSet construction."""
        with pytest.raises(TypeError) as excinfo:
            ValueSet(valueset)

    #test value_set errors
    test_TypeError(1)
    test_TypeError(1.0)
    test_TypeError("")
    test_TypeError(set([]))
    test_TypeError(object)

def test___eq__():
    """Test == operator."""
    VS1, VS2 = ValueSet([]), ValueSet([])
    VS3, VS4 = ValueSet([1]), ValueSet([1])
    assert VS1 == VS2
    assert VS3 == VS4

def test___ne__():
    """Test != operator."""
    VS1, VS2 = ValueSet([]), ValueSet([1])
    assert VS1 != VS2

def test___le__():
    """Test <= operator."""
    VS1, VS2 = ValueSet([]), ValueSet([1])
    VS3, VS4 = ValueSet([1]), ValueSet([1])
    VS5, VS6 = ValueSet([1]), ValueSet([])

    assert VS1 < VS2
    assert VS1 <= VS2
    assert VS3 <= VS4
    assert VS3 >= VS4
    assert VS5 > VS6
    assert VS5 >= VS6

def test___sub__():
    """Test - operator."""
    pass

def test___getitem__():
    """."""
    pass

def test___contains__():
    """."""
    pass

def test___len__():
    """."""
    pass

def test___iter__():
    """."""
    pass

def test___nonzero__():
    """."""
    pass

def test___deepcopy__():
    """."""
    pass

def test___str__():
    """."""
    pass

def test___repr__():
    """."""
    pass

def test__split_by_types():
    """."""
    pass

def test__parse():
    """."""
    pass
