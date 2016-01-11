"""InferenceRules unit tests."""

import pytest

from vivid.Classes.Point import Point
from vivid.Classes.Interval import Interval
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.VariableAssignment import VariableAssignment
from vivid.Classes.NamedState import NamedState
from vivid.Classes.AttributeInterpretation import AttributeInterpretation
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase
from vivid.Classes.Context import Context

from vivid.Classes.InferenceRules import thinning, widening, observe, diagrammatic_absurdity, sentential_absurdity, diagram_reiteration, sentential_to_sentential


def test_thinning():
    """Test thinning."""
    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
    r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                       ['hour', 'minute', 'hour', 'minute'], 3)
    r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                        ['hour', 'minute', 'hour', 'minute'], 4)

    r_one_pm = Relation('R5(h1) <=> h1 = 13', ['hour'], 5)
    r_clock1_3pm_or_before_and_clock2_after_9am = Relation(
        'R6(h1, h2) <=> h1 <= 15 and h2 > 9', ['hour', 'hour'], 6)

    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am, r_one_pm,
        r_clock1_3pm_or_before_and_clock2_after_9am)

    pm_rs = RelationSymbol('PM', 1)
    am_rs = RelationSymbol('AM', 1)
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    one_pm_rs = RelationSymbol('ONE_PM', 1)
    clock1_3pm_or_before_and_clock2_after_9am_rs = RelationSymbol(
        'C1_3PM_&_C2_9AM', 2)
    vocabulary = Vocabulary(['C1', 'C2'],
                            [pm_rs, am_rs, ahead_rs, behind_rs, one_pm_rs,
                             clock1_3pm_or_before_and_clock2_after_9am_rs],
                            ['V1', 'V2'])

    profiles = [
        [pm_rs, ('hour', 1)],
        [am_rs, ('hour', 1)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [one_pm_rs, ('hour', 1)],
        [clock1_3pm_or_before_and_clock2_after_9am_rs, ('hour', 1), ('hour', 2)]]

    attribute_interpretation = AttributeInterpretation(
        vocabulary,
        attribute_structure,
        {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4, one_pm_rs: 5,
         clock1_3pm_or_before_and_clock2_after_9am_rs: 6},
        profiles)

    objs = ['s1', 's2']
    asys = AttributeSystem(attribute_structure, objs)

    const_mapping = {'C1': 's1', 'C2': 's2'}
    p = ConstantAssignment(vocabulary, asys, const_mapping)

    ascriptions_1 = {("hour", "s1"): [13], ("minute", "s1"): [10],
                     ("hour", "s2"): [1, 3, 5, 10], ("minute", "s2"): [10]}

    ascriptions_2 = {("hour", "s1"): [13, 15, 17, 21], ("minute", "s1"): [10],
                     ("hour", "s2"): [1, 3, 5, 10], ("minute", "s2"): [10]}

    ascriptions_3 = {("hour", "s1"): [13, 15], ("minute", "s1"): [10],
                     ("hour", "s2"): [10], ("minute", "s2"): [10]}

    named_state_1 = NamedState(asys, p, ascriptions_1)
    named_state_2 = NamedState(asys, p, ascriptions_2)
    named_state_3 = NamedState(asys, p, ascriptions_3)

    f1 = Formula(vocabulary, 'PM', 'C1')
    f2 = Formula(vocabulary, 'AM', 'C2')
    f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
    assumption_base_1 = AssumptionBase(f1, f2, f3)
    context_1 = Context(assumption_base_1, named_state_2)

    f_one_pm = Formula(vocabulary, 'ONE_PM', 'C1')
    assumption_base_one_pm = AssumptionBase(f_one_pm)
    assert thinning(context_1, named_state_1, assumption_base_one_pm,
                    attribute_interpretation)

    f_clock1_3pm_or_before_and_clock2_after_9am = Formula(
        vocabulary, "C1_3PM_&_C2_9AM", 'C1', 'C2')
    assumption_base_clock1_3pm_or_before_and_clock2_After_9am = \
        AssumptionBase(f_clock1_3pm_or_before_and_clock2_after_9am)

    assert thinning(context_1, named_state_3,
                    assumption_base_clock1_3pm_or_before_and_clock2_After_9am,
                    attribute_interpretation)

    assert thinning(context_1, named_state_1)
    assert thinning(context_1, named_state_2)
    assert thinning(context_1, named_state_3)


def test_widening():
    """Test widening."""
    def test_context_bound():
        """
        Test widening with entailment call when all objects are bound to
        constants via ConstantAssignment.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
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
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1', 'C2': 's2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions_1 = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        ascriptions_2 = {("hour", "s1"): [13, 15, 17, 21], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        ascriptions_3 = {("hour", "s1"): [13, 15], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        named_state_1 = NamedState(asys, p, ascriptions_1)
        named_state_2 = NamedState(asys, p, ascriptions_2)
        named_state_3 = NamedState(asys, p, ascriptions_3)

        f1 = Formula(vocabulary, 'PM', 'C1')
        f2 = Formula(vocabulary, 'AM', 'C2')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        assumption_base_1 = AssumptionBase(f1, f2, f3)
        context_1 = Context(assumption_base_1, named_state_1)

        assert widening(context_1, named_state_1, attribute_interpretation)
        assert widening(context_1, named_state_2, attribute_interpretation)
        assert not widening(context_1, named_state_3, attribute_interpretation)

    def test_context_unbound():
        """
        Test widening with entailment call when not all objects are bound to
        constants, i.e., VariableAssignments come into play.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
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
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2', 's3']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping_2 = {'C1': 's1'}
        p2 = ConstantAssignment(vocabulary, asys, const_mapping_2)

        ascriptions_4 = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        ascriptions_5 = {("hour", "s1"): [13, 15, 17, 21], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        ascriptions_6 = {("hour", "s1"): [13, 15], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        named_state_4 = NamedState(asys, p2, ascriptions_4)
        named_state_5 = NamedState(asys, p2, ascriptions_5)
        named_state_6 = NamedState(asys, p2, ascriptions_6)

        f4 = Formula(vocabulary, 'Behind', 'V1', 'C1')
        assumption_base_2 = AssumptionBase(f4)

        context_2 = Context(assumption_base_2, named_state_4)
        assert widening(context_2, named_state_4, attribute_interpretation)
        assert widening(context_2, named_state_5, attribute_interpretation)
        assert not widening(context_2, named_state_6, attribute_interpretation)

    def test_version_named_state():
        """Do simple widening test."""
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])

        attribute_structure = AttributeStructure(point)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4', 'P5'], [], [])

        objects = ['p1', 'p2', 'p3', 'p4', 'p5']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4',
                                'P5': 'p5'})

        named_state = NamedState(attribute_system, p, {})
        assumption_base = AssumptionBase(vocabulary)

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})
        context_1 = Context(assumption_base, world)
        context_2 = Context(assumption_base, named_state)

        assert widening(context_1, named_state)
        assert widening(context_1, world)
        assert not widening(context_2, world)
        assert widening(context_2, named_state)

    test_version_named_state()
    test_context_bound()
    test_context_unbound()


def test_observe():
    """Test observe function."""
    def test_bounded():
        """Test observe when all objects are bound to a ConstantAssignment."""
        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
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
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1', 'C2': 's2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                       ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        named_state = NamedState(asys, p, ascriptions)

        f1 = Formula(vocabulary, 'PM', 'C1')
        f2 = Formula(vocabulary, 'AM', 'C2')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        f4 = Formula(vocabulary, 'Behind', 'C2', 'C1')
        assumption_base = AssumptionBase(vocabulary)
        context = Context(assumption_base, named_state)

        assert observe(context, f1, attribute_interpretation)
        assert observe(context, f2, attribute_interpretation)
        assert observe(context, f3, attribute_interpretation)
        assert observe(context, f4, attribute_interpretation)

    def test_unbounded():
        """
        Test observe when all objects are not bound in a ConstantAssignment.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation(
            'R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
            ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation(
            'R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)

        vocabulary = Vocabulary(
            ['C1', 'C2'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1'])

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2', 's3']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping_2 = {'C1': 's1'}
        p2 = ConstantAssignment(vocabulary, asys, const_mapping_2)

        ascriptions = {("hour", "s1"): [15, 17, 21], ("minute", "s1"): [10],
                       ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                       ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        named_state = NamedState(asys, p2, ascriptions)

        f_ahead = Formula(vocabulary, 'Ahead', 'C1', 'V1')
        f_behind = Formula(vocabulary, 'Behind', 'V1', 'C1')
        assumption_base = AssumptionBase(vocabulary)

        context = Context(assumption_base, named_state)
        assert observe(context, f_ahead, attribute_interpretation)
        assert observe(context, f_behind, attribute_interpretation)

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_all_behind = Relation(
            'R4(h1,m1,h2,m2,h3,m3,h4,m4) <=> (h1 > h2 or (h1 = h2 and m1 > m2)) and (h1 > h3 or (h1 = h3 and m1 > m3)) and (h1 > h4 or (h1 = h4 and m1 > m4))',
            ['hour', 'minute', 'hour', 'minute', 'hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_all_behind)

        all_behind_rs = RelationSymbol('All behind', 4)

        vocabulary = Vocabulary(
            ['C1'], [all_behind_rs], ['V1', 'V2', 'V3'])

        profiles = [[all_behind_rs,
                     ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2),
                     ('hour', 3), ('minute', 3), ('hour', 4), ('minute', 4)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {all_behind_rs: 4},
            profiles)

        objs = ['s1', 's2', 's3', 's4']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping_2 = {'C1': 's1'}
        p2 = ConstantAssignment(vocabulary, asys, const_mapping_2)

        ascriptions = {("hour", "s1"): [11, 21], ("minute", "s1"): [10],
                       ("hour", "s2"): [7, 9], ("minute", "s2"): [10],
                       ("hour", "s3"): [3, 6], ("minute", "s3"): [40],
                       ("hour", "s4"): [11], ("minute", "s4"): [Interval(6, 9)]}

        named_state = NamedState(asys, p2, ascriptions)

        f_all_behind_1 = Formula(
            vocabulary, 'All behind', 'C1', 'V1', 'V2', 'V3')
        f_all_behind_2 = Formula(
            vocabulary, 'All behind', 'C1', 'V1', 'V3', 'V2')
        f_all_behind_3 = Formula(
            vocabulary, 'All behind', 'C1', 'V2', 'V1', 'V3')
        f_all_behind_4 = Formula(
            vocabulary, 'All behind', 'C1', 'V2', 'V3', 'V1')
        f_all_behind_5 = Formula(
            vocabulary, 'All behind', 'C1', 'V3', 'V1', 'V2')
        f_all_behind_6 = Formula(
            vocabulary, 'All behind', 'C1', 'V3', 'V2', 'V1')

        assumption_base = AssumptionBase(vocabulary)
        context = Context(assumption_base, named_state)

        assert observe(context, f_all_behind_1, attribute_interpretation)
        assert observe(context, f_all_behind_2, attribute_interpretation)
        assert observe(context, f_all_behind_3, attribute_interpretation)
        assert observe(context, f_all_behind_4, attribute_interpretation)
        assert observe(context, f_all_behind_5, attribute_interpretation)
        assert observe(context, f_all_behind_6, attribute_interpretation)

    def test_point():
        """Test observe with Point object."""
        from vivid.Classes.Point import Point
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        rs_is_on = RelationSymbol('IS_ON', 3)
        rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
        rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
        rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4'],
                                [rs_is_on, rs_not_same_point,
                                 rs_clocks_unequal, rs_can_observe],
                                [])

        profiles = [
            [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
            [rs_not_same_point, ('point', 1), ('point', 2)],
            [rs_clocks_unequal, ('point', 1), ('point', 2)],
            [rs_can_observe,
             ('point', 1), ('point', 2), ('point', 3), ('point', 4)]]

        mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
                   rs_can_observe: 4}

        attribute_interpretation = AttributeInterpretation(vocabulary,
                                                           attribute_structure,
                                                           mapping,
                                                           profiles)

        objects = ['p1', 'p2', 'p3', 'p4']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4'})

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5),
                                             Point(1.75, 1.75, 1.75, 1.75)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P1', 'P3', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P2')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P2', 'P3', 'P4')

        context = Context(AssumptionBase(vocabulary), world)

        assert observe(context, f1, attribute_interpretation)
        assert observe(context, f2, attribute_interpretation)
        assert observe(context, f3, attribute_interpretation)
        assert observe(context, f4, attribute_interpretation)

    test_bounded()
    test_unbounded()
    test_point()


def test_diagrammatic_absurdity():
    """Test diagrammatic absurdity."""

    def test_context_bound():
        """
        Test diagrammatic absurdity call when all objects are bound to
        constants via ConstantAssignment.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
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
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1', 'C2': 's2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions_1 = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        ascriptions_2 = {("hour", "s1"): [Interval(3, 19)], ("minute", "s1"): [1],
                         ("hour", "s2"): [10, 14, 4], ("minute", "s2"): [10, 19]}

        named_state_1 = NamedState(asys, p, ascriptions_1)
        named_state_2 = NamedState(asys, p, ascriptions_2)

        f1 = Formula(vocabulary, 'AM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        assumption_base_1 = AssumptionBase(f1, f3)
        context = Context(assumption_base_1, named_state_1)

        assert diagrammatic_absurdity(context, named_state_2,
                                      attribute_interpretation)

        f1 = Formula(vocabulary, 'PM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C2', 'C1')
        assumption_base_1 = AssumptionBase(f1, f3)
        context = Context(assumption_base_1, named_state_1)

        assert diagrammatic_absurdity(context, named_state_2,
                                      attribute_interpretation)

    def test_context_unbound():
        """
        Test diagrammatic absurdity call when not all objects are bound to
        constants, i.e., VariableAssignments come into play.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)

        vocabulary = Vocabulary(
            ['C1'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2', 's3']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions_5 = {("hour", "s1"): [13, 15, 17, 21], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        ascriptions_6 = {("hour", "s1"): [13, 15], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        named_state_5 = NamedState(asys, p, ascriptions_5)
        named_state_6 = NamedState(asys, p, ascriptions_6)

        f_behind = Formula(vocabulary, 'Behind', 'V1', 'C1')
        assumption_base = AssumptionBase(f_behind)
        context = Context(assumption_base, named_state_5)

        # No VariableAssignment provided so truth value unknown and absurdity
        # does not hold
        assert not diagrammatic_absurdity(context, named_state_6,
                                          attribute_interpretation)

        X = VariableAssignment(vocabulary, asys, {'V1': 's2'})
        f_behind = Formula(vocabulary, 'Behind', 'C1', 'V1')
        assumption_base = AssumptionBase(f_behind)
        context = Context(assumption_base, named_state_5)

        # VariableAssignment provided so truth value is known and f_behind
        # evaluates to False so absurdity holds
        assert diagrammatic_absurdity(context, NamedState(asys, p),
                                      attribute_interpretation, X)

    def test_point():
        """Test diagrammatic absurdity with Point object."""
        from vivid.Classes.Point import Point
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        rs_is_on = RelationSymbol('IS_ON', 3)
        rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
        rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
        rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4'],
                                [rs_is_on, rs_not_same_point,
                                 rs_clocks_unequal, rs_can_observe],
                                [])

        profiles = [
            [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
            [rs_not_same_point, ('point', 1), ('point', 2)],
            [rs_clocks_unequal, ('point', 1), ('point', 2)],
            [rs_can_observe,
             ('point', 1), ('point', 2), ('point', 3), ('point', 4)]]

        mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
                   rs_can_observe: 4}

        attribute_interpretation = AttributeInterpretation(vocabulary,
                                                           attribute_structure,
                                                           mapping,
                                                           profiles)

        objects = ['p1', 'p2', 'p3', 'p4']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4'})

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5),
                                             Point(1.75, 1.75, 1.75, 1.75)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P3', 'P1', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P2', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P1')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P3', 'P2', 'P4')

        assumption_base = AssumptionBase(f1)
        context = Context(assumption_base, world)
        assert diagrammatic_absurdity(context, NamedState(attribute_system, p),
                                      attribute_interpretation)

        assumption_base = AssumptionBase(f2)
        context = Context(assumption_base, world)
        assert diagrammatic_absurdity(context, NamedState(attribute_system, p),
                                      attribute_interpretation)

        assumption_base = AssumptionBase(f3)
        context = Context(assumption_base, world)
        assert diagrammatic_absurdity(context, NamedState(attribute_system, p),
                                      attribute_interpretation)

        assumption_base = AssumptionBase(f4)
        context = Context(assumption_base, world)
        assert diagrammatic_absurdity(context, NamedState(attribute_system, p),
                                      attribute_interpretation)

    test_context_bound()
    test_context_unbound()
    test_point()


def test_sentential_absurdity():
    """Test sentential absurdity."""
    def test_context_bound():
        """
        Test sentential absurdity call when all objects are bound to
        constants via ConstantAssignment.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
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
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1', 'C2': 's2'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions_1 = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

        ascriptions_2 = {("hour", "s1"): [Interval(3, 19)], ("minute", "s1"): [1],
                         ("hour", "s2"): [10, 14, 4], ("minute", "s2"): [10, 19]}

        named_state_1 = NamedState(asys, p, ascriptions_1)
        named_state_2 = NamedState(asys, p, ascriptions_2)

        f1 = Formula(vocabulary, 'AM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C1', 'C2')
        assumption_base_1 = AssumptionBase(f1, f3)
        context = Context(assumption_base_1, named_state_1)

        assert sentential_absurdity(context, Formula(vocabulary, 'AM', 'V1'),
                                    attribute_interpretation)

        f1 = Formula(vocabulary, 'PM', 'C1')
        f3 = Formula(vocabulary, 'Ahead', 'C2', 'C1')
        assumption_base_1 = AssumptionBase(f1, f3)
        context = Context(assumption_base_1, named_state_1)

        assert sentential_absurdity(context, Formula(vocabulary, 'AM', 'V1'),
                                    attribute_interpretation)

    def test_context_unbound():
        """
        Test sentential absurdity call when not all objects are bound to
        constants, i.e., VariableAssignments come into play.
        """

        a = Attribute('hour', [Interval(0, 23)])
        a2 = Attribute('minute', [Interval(0, 59)])
        r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
        r_am = Relation('R2(h1) <=> h1 <= 11', ['hour'], 2)
        r_ahead = Relation('R3(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                           ['hour', 'minute', 'hour', 'minute'], 3)
        r_behind = Relation('R4(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                            ['hour', 'minute', 'hour', 'minute'], 4)
        attribute_structure = AttributeStructure(
            a, a2, r_ahead, r_behind, r_pm, r_am)

        pm_rs = RelationSymbol('PM', 1)
        am_rs = RelationSymbol('AM', 1)
        ahead_rs = RelationSymbol('Ahead', 4)
        behind_rs = RelationSymbol('Behind', 4)

        vocabulary = Vocabulary(
            ['C1'], [pm_rs, am_rs, ahead_rs, behind_rs], ['V1', 'V2'])

        profiles = [
            [pm_rs, ('hour', 1)],
            [am_rs, ('hour', 1)],
            [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
            [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)]]

        attribute_interpretation = AttributeInterpretation(
            vocabulary,
            attribute_structure,
            {pm_rs: 1, am_rs: 2, ahead_rs: 3, behind_rs: 4},
            profiles)

        objs = ['s1', 's2', 's3']
        asys = AttributeSystem(attribute_structure, objs)

        const_mapping = {'C1': 's1'}
        p = ConstantAssignment(vocabulary, asys, const_mapping)

        ascriptions_5 = {("hour", "s1"): [13, 15, 17, 21], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        ascriptions_6 = {("hour", "s1"): [13, 15], ("minute", "s1"): [10],
                         ("hour", "s2"): [1, 3, 5, 9], ("minute", "s2"): [10],
                         ("hour", "s3"): [1, 3, 5], ("minute", "s3"): [10]}

        named_state_5 = NamedState(asys, p, ascriptions_5)
        named_state_6 = NamedState(asys, p, ascriptions_6)

        f_behind = Formula(vocabulary, 'Behind', 'V1', 'C1')
        assumption_base = AssumptionBase(f_behind)
        context = Context(assumption_base, named_state_5)

        # No VariableAssignment provided so truth value unknown and absurdity
        # does not hold
        assert not sentential_absurdity(context, Formula(vocabulary, 'AM', 'V1'),
                                        attribute_interpretation)

        X = VariableAssignment(vocabulary, asys, {'V1': 's2'})
        f_behind = Formula(vocabulary, 'Behind', 'C1', 'V1')
        assumption_base = AssumptionBase(f_behind)
        context = Context(assumption_base, named_state_5)

        # VariableAssignment provided so truth value is known and f_behind
        # evaluates to False so absurdity holds
        assert sentential_absurdity(context, Formula(vocabulary, 'AM', 'V1'),
                                    attribute_interpretation, X)

    def test_point():
        """Test sentential absurdity with Point object."""
        from vivid.Classes.Point import Point
        point = Attribute('point', [Point('x', 'x', 'x', 'x')])
        r_is_on = Relation('R1(h1, h2, h3) <=> is_on(h1, h2, h3)',
                           ['point', 'point', 'point'], 1)
        r_not_same_point = Relation('R2(h1, h2) <=> not_same_point(h1, h2)',
                                    ['point', 'point'], 2)
        r_clocks_unequal = Relation('R3(h1, h2) <=> clocks_unequal(h1, h2)',
                                    ['point', 'point'], 3)
        r_can_observe = Relation(
            'R4(p, sp_loc, wls, wle) <=> can_observe(p, sp_loc, wls, wle)',
            ['point', 'point', 'point', 'point'], 4)

        attribute_structure = AttributeStructure(
            point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe)

        rs_is_on = RelationSymbol('IS_ON', 3)
        rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
        rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
        rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)

        vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4'],
                                [rs_is_on, rs_not_same_point,
                                 rs_clocks_unequal, rs_can_observe],
                                [])

        profiles = [
            [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
            [rs_not_same_point, ('point', 1), ('point', 2)],
            [rs_clocks_unequal, ('point', 1), ('point', 2)],
            [rs_can_observe,
             ('point', 1), ('point', 2), ('point', 3), ('point', 4)]]

        mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
                   rs_can_observe: 4}

        attribute_interpretation = AttributeInterpretation(vocabulary,
                                                           attribute_structure,
                                                           mapping,
                                                           profiles)

        objects = ['p1', 'p2', 'p3', 'p4']
        attribute_system = AttributeSystem(attribute_structure, objects)
        p = ConstantAssignment(vocabulary, attribute_system,
                               {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4'})

        world = NamedState(attribute_system, p, {
                           ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5),
                                             Point(1.75, 1.75, 1.75, 1.75)],
                           ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                           ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                           ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)]})

        f1 = Formula(vocabulary, 'IS_ON', 'P3', 'P1', 'P4')
        f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P2', 'P2')
        f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P1')
        f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P3', 'P2', 'P4')

        assumption_base = AssumptionBase(f1)
        context = Context(assumption_base, world)
        assert sentential_absurdity(context,
                                    Formula(vocabulary, "NOT_SAME_POINT",
                                            'P1', 'P1'),
                                    attribute_interpretation)

        assumption_base = AssumptionBase(f2)
        context = Context(assumption_base, world)
        assert sentential_absurdity(context,
                                    Formula(vocabulary, "NOT_SAME_POINT",
                                            'P1', 'P1'),
                                    attribute_interpretation)

        assumption_base = AssumptionBase(f3)
        context = Context(assumption_base, world)
        assert sentential_absurdity(context,
                                    Formula(vocabulary, "NOT_SAME_POINT",
                                            'P1', 'P1'),
                                    attribute_interpretation)

        assumption_base = AssumptionBase(f4)
        context = Context(assumption_base, world)
        assert sentential_absurdity(context,
                                    Formula(vocabulary, "NOT_SAME_POINT",
                                            'P1', 'P1'),
                                    attribute_interpretation)

    test_context_bound()
    test_context_unbound()
    test_point()


def test_diagram_reiteration():
    """Test diagramm reiteration."""
    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    attribute_structure = AttributeStructure(a, a2)

    vocabulary = Vocabulary(['C1', 'C2'], [], [])

    objs = ['s1', 's2']
    asys = AttributeSystem(attribute_structure, objs)

    const_mapping = {'C1': 's1', 'C2': 's2'}
    p = ConstantAssignment(vocabulary, asys, const_mapping)

    ascriptions = {("hour", "s1"): [13, 15, 17], ("minute", "s1"): [10],
                   ("hour", "s2"): [1, 3, 5], ("minute", "s2"): [10]}

    named_state = NamedState(asys, p, ascriptions)

    assumption_base = AssumptionBase(vocabulary)
    context = Context(assumption_base, named_state)

    d1 = diagram_reiteration(context)
    assert context._named_state is d1


def test_sentential_to_sentential():
    """Test sentential_to_sentential rule."""
    def test_ValueError(context, F1, F2, G, attribute_interpretation):
        """Test constructor for ValueErrors with given params."""
        with pytest.raises(ValueError) as excinfo:
            sentential_to_sentential(
                context, F1, F2, G, attribute_interpretation)

    a = Attribute('hour', [Interval(0, 23)])
    a2 = Attribute('minute', [Interval(0, 59)])
    r_pm = Relation('R1(h1) <=> h1 > 11', ['hour'], 1)
    r_one_pm = Relation(
        'R2(h1, m1) <=> h1 = 13 and m1 = 0', ['hour', 'minute'], 2)
    r_three_pm = Relation(
        'R3(h1, m1) <=> h1 = 15 and m1 = 0', ['hour', 'minute'], 3)
    attribute_structure = AttributeStructure(
        a, a2, r_pm, r_one_pm, r_three_pm)

    pm_rs = RelationSymbol('PM', 1)
    one_pm_rs = RelationSymbol('ONE_PM', 2)
    three_pm_rs = RelationSymbol('THREE_PM', 2)
    vocabulary = Vocabulary(
        ['C1'], [pm_rs, one_pm_rs, three_pm_rs], ['V1'])

    profiles = [
        [pm_rs, ('hour', 1)],
        [one_pm_rs, ('hour', 1), ('minute', 1)],
        [three_pm_rs, ('hour', 1), ('minute', 1)]]

    attribute_interpretation = AttributeInterpretation(
        vocabulary,
        attribute_structure,
        {pm_rs: 1, one_pm_rs: 2, three_pm_rs: 3},
        profiles)

    objs = ['s1']
    asys = AttributeSystem(attribute_structure, objs)

    const_mapping = {'C1': 's1'}
    p = ConstantAssignment(vocabulary, asys, const_mapping)

    ascriptions = {("hour", "s1"): [13, 15], ("minute", "s1"): [0]}
    named_state = NamedState(asys, p, ascriptions)

    f_one_pm = Formula(vocabulary, "ONE_PM", 'C1')
    f_three_pm = Formula(vocabulary, "THREE_PM", 'C1')
    f_pm = Formula(vocabulary, "PM", 'C1')

    assumption_base = AssumptionBase(vocabulary)
    context = Context(assumption_base, named_state)

    # Truth value is unknown for f_one_pm and f_three_pm so disjunction
    # doesn't hold
    test_ValueError(context, f_one_pm, f_three_pm, f_pm,
                    attribute_interpretation)

    ascriptions = {("hour", "s1"): [15], ("minute", "s1"): [0]}
    named_state = NamedState(asys, p, ascriptions)
    context = Context(assumption_base, named_state)

    assert sentential_to_sentential(context, f_one_pm, f_three_pm, f_pm,
                                    attribute_interpretation)
    assert sentential_to_sentential(context, f_three_pm, f_one_pm, f_pm,
                                    attribute_interpretation)
    assert not sentential_to_sentential(context, f_three_pm, f_pm, f_one_pm,
                                        attribute_interpretation)
    # In the case of the assumption base containing f_one_pm, entailment holds
    # as it's a case of absurdity
    assert sentential_to_sentential(context, f_one_pm, f_pm, f_three_pm,
                                    attribute_interpretation)

    var_mapping = {'V1': 's1'}
    X = VariableAssignment(vocabulary, asys, var_mapping)
    f_three_pm = Formula(vocabulary, "THREE_PM", 'V1')
    f_one_pm = Formula(vocabulary, "ONE_PM", 'V1')

    assert sentential_to_sentential(context, f_one_pm, f_three_pm, f_pm,
                                    attribute_interpretation, X)
    assert sentential_to_sentential(context, f_three_pm, f_one_pm, f_pm,
                                    attribute_interpretation, X)
    assert not sentential_to_sentential(context, f_three_pm, f_pm, f_one_pm,
                                        attribute_interpretation, X)
    assert sentential_to_sentential(context, f_one_pm, f_pm, f_three_pm,
                                    attribute_interpretation, X)

    # Now there's no constants bound
    named_state = NamedState(asys, ConstantAssignment(vocabulary, asys, {}),
                             ascriptions)
    context = Context(assumption_base, named_state)

    f_one_pm = Formula(vocabulary, "ONE_PM", 'V1')
    f_three_pm = Formula(vocabulary, "THREE_PM", 'V1')
    f_pm = Formula(vocabulary, "PM", 'V1')

    assert sentential_to_sentential(context, f_one_pm, f_three_pm, f_pm,
                                    attribute_interpretation, X)
    assert sentential_to_sentential(context, f_three_pm, f_one_pm, f_pm,
                                    attribute_interpretation, X)
    assert not sentential_to_sentential(context, f_three_pm, f_pm, f_one_pm,
                                        attribute_interpretation, X)
    assert sentential_to_sentential(context, f_one_pm, f_pm, f_three_pm,
                                    attribute_interpretation, X)

    test_ValueError(context, f_one_pm, f_three_pm, f_pm,
                    attribute_interpretation)
    test_ValueError(context, f_three_pm, f_one_pm, f_pm,
                    attribute_interpretation)
    test_ValueError(context, f_three_pm, f_pm, f_one_pm,
                    attribute_interpretation)
    test_ValueError(context, f_one_pm, f_pm, f_three_pm,
                    attribute_interpretation)
