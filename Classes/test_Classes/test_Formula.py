"""Formula unit tests."""

import pytest

from vivid.Classes.Interval import Interval
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.NamedState import NamedState
from vivid.Classes.AttributeInterpretation import AttributeInterpretation
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.VariableAssignment import VariableAssignment
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase


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
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

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


def test___add__():
    """Test + operator for Formula object."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, am_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1', 'V1')
    f3 = Formula(vocabulary, 'PM', 'C1')
    f4 = Formula(vocabulary, 'AM', 'C1')
    a1 = AssumptionBase(f1, f2)

    a = f1 + f2
    a = f2 + f1
    assert hasattr(a, "_is_AssumptionBase")
    a = f3 + a1
    assert hasattr(a, "_is_AssumptionBase")

    a = f1 + f2 + f3 + f4
    assert hasattr(a, "_is_AssumptionBase")
    assert len(a) == 4


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


def test__key():
    """Test key for hash function."""
    C, R, V = ['C'], [RelationSymbol('R', 1)], ['V']
    vocabulary = Vocabulary(C, R, V)

    formula = Formula(vocabulary, 'R', 'C', 'V')
    assert (hash(vocabulary), 'R', ('C', 'V')) == formula._key()


def test___hash__():
    """Test hash(Vocabulary)."""
    C, R, V = ['C'], [RelationSymbol('R', 1)], ['V']
    vocabulary = Vocabulary(C, R, V)

    formula1 = Formula(vocabulary, 'R', 'C', 'V')
    formula2 = Formula(vocabulary, 'R', 'V', 'C')

    assert hash(formula1) == hash(formula2)


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


def test_assign_truth_value():
    """Test assign_truth_value() function of Formula object."""
    def test_TypeError(formula, attribute_interpretation, named_state, X):
        """Test TypeError catching in assign_truth_value()."""
        with pytest.raises(TypeError) as excinfo:
            formula.assign_truth_value(
                attribute_interpretation, named_state, X)

    def test_ValueError(formula, attribute_interpretation, named_state, X):
        """Test ValueError catching in assign_truth_value()."""
        with pytest.raises(ValueError) as excinfo:
            formula.assign_truth_value(
                attribute_interpretation, named_state, X)

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation(
        'R3(h1,m1,hhh2,mm2) <=> h1 > hhh2 or (h1 = hhh2 and m1 > mm2)',
        ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation(
        'R4(h1,m1,h2,m2) <=> h1 <= h2 or (h1 = h2 and m1 < m2)',
        ['hour', 'minute', 'hour', 'minute'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

    profiles = [
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

    bad_profiles = [
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [ahead_rs, ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

    mapping = {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4}

    attribute_interpretation = AttributeInterpretation(
        vocabulary, attribute_structure, mapping, profiles)

    objects = ['s1', 's2']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(
        vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    named_state = NamedState(attribute_system, p, {
                             ('hour', 's1'): [9, 13],
                             ('minute', 's1'): [12],
                             ('hour', 's2'): [8],
                             ('minute', 's2'): [27]})

    f = Formula(vocabulary, 'Ahead', 'C1', 'C2')

    VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

    bad_vocabulary = Vocabulary(
        ['C1', 'C2', 'C3'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])
    bad_p = ConstantAssignment(
        bad_vocabulary, attribute_system, {'C1': 's1', 'C2': 's2'})
    bad_f = Formula(bad_vocabulary, 'Ahead', 'C1', 'C2')
    bad_t_f = Formula(bad_vocabulary, 'Ahead', 'C1')
    bad_v_attribute_interpretation = AttributeInterpretation(
        bad_vocabulary, attribute_structure, mapping, profiles)
    bad_p_attribute_interpretation = AttributeInterpretation(
        vocabulary, attribute_structure, mapping, bad_profiles)
    bad_named_state = NamedState(attribute_system, bad_p, {})
    bad_VA = VariableAssignment(
        bad_vocabulary, attribute_system, {}, dummy=True)

    # Test invalid types
    test_TypeError(f, None, named_state, VA)
    test_TypeError(f, object, named_state, VA)
    test_TypeError(f, attribute_interpretation, None, VA)
    test_TypeError(f, attribute_interpretation, object, VA)
    test_TypeError(f, attribute_interpretation, named_state, None)
    test_TypeError(f, attribute_interpretation, named_state, object)
    # Test mismatched vocabularies
    test_ValueError(bad_f, attribute_interpretation, named_state, VA)
    test_ValueError(f, bad_v_attribute_interpretation, named_state, VA)
    test_ValueError(bad_f, attribute_interpretation, bad_named_state, VA)
    test_ValueError(f, attribute_interpretation, named_state, bad_VA)
    # Test profile length, DR length mismatch
    test_ValueError(f, bad_p_attribute_interpretation, named_state, VA)
    # Test profile j_x against length of terms
    test_ValueError(bad_t_f, attribute_interpretation, named_state, VA)
    assert f.assign_truth_value(attribute_interpretation, named_state, VA)
