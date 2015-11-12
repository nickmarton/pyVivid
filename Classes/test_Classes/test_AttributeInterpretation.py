"""Attribute Interpretation unit tests."""

import pytest
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.AttributeInterpretation import AttributeInterpretation

def test___init__():
    """Test AttributeInterpretation constructor."""
    def test_TypeError(vocabulary, attribute_structure, mapping, profiles):
        """Test TypeError catching in AttributeInterpretation constructor."""
        with pytest.raises(TypeError) as excinfo:
            AttributeInterpretation(vocabulary, attribute_structure, mapping,
                                                                    profiles)
    def test_ValueError(vocabulary, attribute_structure, mapping, profiles):
        """Test ValueError catching in AttributeInterpretation constructor."""
        with pytest.raises(ValueError) as excinfo:
            AttributeInterpretation(vocabulary, attribute_structure, mapping,
                                                                    profiles)

    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]]
    bad_profiles = [
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]]
    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}
    bad_source_mapping = {ahead_rs: 1, "behind_rs": 2, pm_rs: 3}
    bad_target_mapping = {ahead_rs: 1, behind_rs: 'R2', pm_rs: 3}
    bad_target_mapping2 = {ahead_rs: 1, behind_rs: 2.0, pm_rs: 3}
    dup_subscr_mapping = {ahead_rs: 2, behind_rs: 2, pm_rs: 3}

    ai = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    
    test_TypeError(None, attribute_structure, mapping, profiles)
    test_TypeError(object, attribute_structure, mapping, profiles)
    test_TypeError(vocabulary, None, mapping, profiles)
    test_TypeError(vocabulary, object, mapping, profiles)
    test_TypeError(vocabulary, AttributeSystem(attribute_structure, ['o']), mapping, profiles)
    test_TypeError(vocabulary, attribute_structure, None, profiles)
    test_TypeError(vocabulary, attribute_structure, object, profiles)
    test_TypeError(vocabulary, attribute_structure, mapping, None)
    test_TypeError(vocabulary, attribute_structure, mapping, object)

    test_ValueError(vocabulary, attribute_structure, bad_source_mapping, profiles)
    test_ValueError(vocabulary, attribute_structure, bad_target_mapping, profiles)
    test_ValueError(vocabulary, attribute_structure, bad_target_mapping2, profiles)

    
    test_ValueError(vocabulary, attribute_structure, mapping, bad_profiles)
    test_ValueError(vocabulary, attribute_structure, dup_subscr_mapping, profiles)
    

    bad_mapping = {RelationSymbol("not in Vocabulary or profiles", 2): 1, behind_rs: 2, pm_rs: 3}
    test_ValueError(vocabulary, attribute_structure, bad_mapping, profiles)
    bad_vocabulary = Vocabulary(
        ['C1', 'C2'],
        [ahead_rs, behind_rs, pm_rs, RelationSymbol("not in source or profiles", 2)],
        ['V1', 'V2'])
    test_ValueError(bad_vocabulary, attribute_structure, mapping, profiles)
    bad_target_mapping = {ahead_rs: 1, behind_rs: 6, pm_rs: 3}
    test_ValueError(vocabulary, attribute_structure, bad_target_mapping, profiles)


    bad_profiles = [
        [ahead_rs, ('doesn\'t exist', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]]
    test_ValueError(vocabulary, attribute_structure, mapping, bad_profiles)
    bad_profiles = [
        [ahead_rs, ('hour', 10), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]]
    test_ValueError(vocabulary, attribute_structure, mapping, bad_profiles)

    AI = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    assert AI._attribute_structure == attribute_structure
    assert AI._attribute_structure is not attribute_structure
    assert AI._vocabulary == vocabulary
    assert AI._vocabulary is not vocabulary

def test___eq__():
    """Test == operator for AttributeInterpretation object."""
    def test_TypeError(ai1, ai2):
        """Test TypeError in == operator for AttributeInterpretation."""
        with pytest.raises(TypeError) as excinfo:
            ai1 == ai2

    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]
    profiles2 = [
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]
    ]
    profiles3 = [
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [ahead_rs, ('hour', 1)],
        [pm_rs, ('hour', 1), ('minute', 1), ('hour', 1), ('minute', 1)]
    ]
    profiles4 = [
        [ahead_rs, ('hour', 2), ('minute', 2), ('hour', 1), ('minute', 1)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]
    profiles5 = [
        [ahead_rs, ('minute', 1), ('hour', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai1 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    ai2 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles2)
    ai3 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles3)
    ai4 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles4)
    ai5 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles5)

    assert ai1 == ai1
    assert ai1 == ai2
    assert not ai1 == ai3
    assert not ai1 == ai4
    assert not ai1 == ai5

def test___ne__():
    """Test != operator for AttributeInterpretation object."""
    def test_TypeError(ai1, ai2):
        """Test TypeError in != operator for AttributeInterpretation."""
        with pytest.raises(TypeError) as excinfo:
            ai1 == ai2

    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]
    profiles2 = [
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]
    ]
    profiles3 = [
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [ahead_rs, ('hour', 1)],
        [pm_rs, ('hour', 1), ('minute', 1), ('hour', 1), ('minute', 1)]
    ]
    profiles4 = [
        [ahead_rs, ('hour', 2), ('minute', 2), ('hour', 1), ('minute', 1)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]
    profiles5 = [
        [ahead_rs, ('minute', 1), ('hour', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai1 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    ai2 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles2)
    ai3 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles3)
    ai4 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles4)
    ai5 = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles5)

    assert not ai1 != ai1
    assert not ai1 != ai2
    assert ai1 != ai3
    assert ai1 != ai4
    assert ai1 != ai5

def test___deepcopy__():
    """Test copy.deepcopy for AttributeInterpretation object."""
    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)

    from copy import deepcopy
    ai_copy = deepcopy(ai)
    assert ai == ai_copy
    assert ai is not ai_copy
    assert ai._vocabulary is not ai_copy._vocabulary
    assert ai._attribute_structure is not ai_copy._attribute_structure
    assert ai._mapping is not ai_copy._mapping
    assert ai._profiles is not ai_copy._profiles
    assert ai._table is not ai_copy._table
    assert ai._relation_symbols is not ai_copy._relation_symbols


def test___str__():
    """Test str(AttributeInterpretation)."""
    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    assert str(ai) == "[Ahead, 4, 'R1', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]\n" + \
                      "[Behind, 4, 'R2', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]\n" + \
                      "[PM, 1, 'R3', [('hour', 1)]]"

def test___repr__():
    """Test repr(AttributeInterpretation)."""
    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)', ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)', ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai = AttributeInterpretation(vocabulary, attribute_structure, mapping, profiles)
    assert repr(ai) == "[Ahead, 4, 'R1', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]\n" + \
                       "[Behind, 4, 'R2', [('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]\n" + \
                       "[PM, 1, 'R3', [('hour', 1)]]"
