"""Formula unit tests."""

import pytest

from vivid.Classes.Formula import Formula
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary

def test___init__():
    """Test Formula constructor."""
    def test_TypeError(vocabulary, name, *terms):
        """Test TypeError catching in Formula constructor."""
        with pytest.raises(TypeError) as excinfo:
            Formula(vocabulary, name, *terms)
    def test_ValueError(vocabulary, name, *terms):
        """Test ValueError catching in Formula constructor."""
        with pytest.raises(ValueError) as excinfo:
            Formula(vocabulary, name, *terms)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])
    
    test_TypeError(None, 'Ahead', 'C1', 'V1')
    test_TypeError(object, 'Ahead', 'C1', 'V1')
    test_TypeError(vocabulary, None, 'C1', 'V1')
    test_TypeError(vocabulary, object, 'C1', 'V1')
    test_ValueError(vocabulary, 'Ahead')
    test_ValueError(vocabulary, 'Ahead', 'nope')

    F = Formula(vocabulary, 'Ahead', 'C1', 'C1', 'C1')
    assert F._terms == ['C1']

def test___eq__():
    """Test == operator for Formula object."""
    def test_TypeError(f1, f2):
        """Test TypeError catching in == operator of Formula."""
        with pytest.raises(TypeError) as excinfo:
            f1 == f2

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(['C1', 'C2', 'C3'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f1 = Formula(vocabulary, 'Ahead', 'C1')
    f2 = Formula(vocabulary, 'Ahead', 'V1', 'C1')
    f3 = Formula(vocabulary, 'Ahead', 'V1', 'C1', 'V1', 'C1')
    f4 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f5 = Formula(vocabulary2, 'Ahead', 'C1', 'V1')

    test_TypeError(f, None)
    test_TypeError(f, object)

    assert f == f
    assert not f == f1
    assert f == f2
    assert f == f3
    assert not f == f4
    assert not f == f5

def test___ne__():
    """Test != operator for Formula object."""
    def test_TypeError(f1, f2):
        """Test TypeError catching in != operator of Formula."""
        with pytest.raises(TypeError) as excinfo:
            f1 != f2

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(['C1', 'C2', 'C3'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f1 = Formula(vocabulary, 'Ahead', 'C1')
    f2 = Formula(vocabulary, 'Ahead', 'V1', 'C1')
    f3 = Formula(vocabulary, 'Ahead', 'V1', 'C1', 'V1', 'C1')
    f4 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f5 = Formula(vocabulary2, 'Ahead', 'C1', 'V1')

    test_TypeError(f, None)
    test_TypeError(f, object)

    assert not f != f
    assert f != f1
    assert not f != f2
    assert not f != f3
    assert f != f4
    assert f != f5

def test___deepcopy__():
    """Test Test copy.deepcopy for Formula object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    from copy import deepcopy
    f_copy = deepcopy(f)

    assert f == f_copy
    assert f is not f_copy
    assert f._vocabulary is not f_copy._vocabulary
    assert f._terms is not f_copy._terms

    f._name = "F"
    assert f._name != f_copy._name

def test___str__():
    """Test str(Formula)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    assert str(f) == "Ahead(C1, V1)"

def test___repr__():
    """Test repr(Formula)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')

    assert repr(f) == "Ahead(C1, V1)"
