"""AssumptionBase unit tests."""

import pytest
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase


def test___init__():
    """Test AssumptionBase constructor."""
    def test_TypeError(*formulae):
        """Test TypeError catching in AssumptionBase constructor."""
        with pytest.raises(TypeError) as excinfo:
            AssumptionBase(*formulae)

    def test_ValueError(*formulae):
        """Test ValueError catching in AssumptionBase constructor."""
        with pytest.raises(ValueError) as excinfo:
            AssumptionBase(*formulae)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary2, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3)

    test_TypeError(f1, None)
    test_TypeError(f1, object)
    test_ValueError(f1, f1)
    test_ValueError(f1, f4)

    assert a1[0] is f1
    assert a1[1] is f2
    assert a1[2] is f3


def test___eq__():
    """Test == operator for AssumptionBase objects."""
    def test_TypeError(self, other):
        """Test TypeError catching in == operator for AssumptionBase."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)
    a2 = AssumptionBase(f2, f4, f1, f3)
    a3 = AssumptionBase(f2, f1, f3)

    test_TypeError(a1, None)
    test_TypeError(a1, f1)
    assert a1 == a1
    assert a1 is a1
    assert a1 == a2
    assert a1 is not a2
    assert not a1 == a3


def test___ne__():
    """Test != operator for AssumptionBase objects."""
    def test_TypeError(self, other):
        """Test TypeError catching in != operator for AssumptionBase."""
        with pytest.raises(TypeError) as excinfo:
            self != other

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)
    a2 = AssumptionBase(f2, f4, f1, f3)
    a3 = AssumptionBase(f2, f1, f3)

    test_TypeError(a1, None)
    test_TypeError(a1, f1)
    assert not a1 != a1
    assert a1 is a1
    assert not a1 != a2
    assert a1 is not a2
    assert a1 != a3


def test___add__():
    """Test + operator for AssumptionBase object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    test_rs = RelationSymbol('test', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'],
        [ahead_rs, behind_rs, am_rs, pm_rs, test_rs],
        ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a_1 = AssumptionBase(f1)
    a_2 = AssumptionBase(f2)
    a_3 = AssumptionBase(f3)
    a_1_2 = AssumptionBase(f1, f2)
    a_1_2_3 = AssumptionBase(f1, f2, f3)
    a_1_2_3_4 = AssumptionBase(f1, f2, f3, f4)

    assert a_1_2 == a_1 + f2
    assert a_1_2 == f2 + a_1
    assert a_1_2 is not a_1
    assert a_1_2 is not f2
    ref_a = a_1 + f2
    f2._name = "test"
    assert ref_a[-1]._name != f2._name
    assert a_1_2 == a_1 + a_2
    assert a_1_2_3 == a_1 + a_2 + a_3
    assert a_1_2_3 == a_1 + f2 + f3
    assert a_1_2_3_4 == a_1 + f2 + f3 + f4


def test___iadd__():
    """Test + operator for AssumptionBase object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    test_rs = RelationSymbol('test', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'],
        [ahead_rs, behind_rs, am_rs, pm_rs, test_rs],
        ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a_1 = AssumptionBase(f1)
    a_2 = AssumptionBase(f2)
    a_3 = AssumptionBase(f3)
    a_1_2 = AssumptionBase(f1, f2)
    a_1_2_3 = AssumptionBase(f1, f2, f3)
    a_1_2_3_4 = AssumptionBase(f1, f2, f3, f4)

    a_1 += a_2
    assert a_1 == a_1_2
    assert a_1 is not a_1_2
    a_1 += (f3 + f4)
    assert a_1 == a_1_2_3_4
    assert a_1 is not a_1_2_3_4


def test___str__():
    """Test str(AssumptionBase)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)

    assert str(a1) == "AB(AM(C1), Ahead(C1, V1), Behind(C1, V1), PM(C1))"


def test___repr__():
    """Test repr(AssumptionBase)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)

    assert repr(a1) == "AB(AM(C1), Ahead(C1, V1), Behind(C1, V1), PM(C1))"


def test___len__():
    """Test len(AssumptionBase)."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)

    assert len(a1) == 4


def test___getitem__():
    """Test indexing of AssumptionBase object."""
    def test_KeyError(assumption_base, key):
        """Test KeyError catching in AssumptionBase constructor."""
        with pytest.raises(KeyError) as excinfo:
            assumption_base[key]

    def test_IndexError(assumption_base, key):
        """Test IndexError catching in AssumptionBase constructor."""
        with pytest.raises(IndexError) as excinfo:
            assumption_base[key]

    def test_TypeError(assumption_base, key):
        """Test TypeError catching in AssumptionBase constructor."""
        with pytest.raises(TypeError) as excinfo:
            assumption_base[key]

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a = AssumptionBase(f1, f2, f3)

    test_TypeError(a, None)
    test_TypeError(a, object)
    test_KeyError(a, 'AM')
    test_KeyError(a, f4)
    test_IndexError(a, 4)
    test_IndexError(a, 1000)

    assert a[f1] is f1
    assert a['Behind'] is f2
    assert a[2] is f3


def test___iter__():
    """Test iterator for AssumptionBase."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3, f4)

    assert set([f1, f2, f3, f4]) == set([f for f in a1])
    assert set([f1, f2, f3, f4]) == set([f for f in iter(a1)])
    assert set([f1, f2, f3, f4]) == set(a1)
    assert set([f1, f2, f3, f4]) == set(iter(a1))


def test___contains__():
    """Test in and not in operators for AssumptionBase object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2, f3)

    assert f1 in a1
    assert f2 in a1
    assert f3 in a1
    assert f4 not in a1


def test___deepcopy__():
    """Test copy.deepcopy for AssumptionBase object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])
    vocabulary2 = Vocabulary(
        ['C1', 'C2', 'C3'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a = AssumptionBase(f1, f2, f3, f4)

    from copy import deepcopy
    a_copy = deepcopy(a)

    assert a == a_copy
    assert a is not a_copy
    assert a._formulae[0] is not a_copy._formulae[0]
    assert a._formulae[1] is not a_copy._formulae[1]
    assert a._formulae[2] is not a_copy._formulae[2]
    assert a._formulae[3] is not a_copy._formulae[3]
