"""InferenceRules unit tests."""

from vivid.Classes.Point import Point
from vivid.Classes.Interval import Interval
from vivid.Classes.Attribute import Attribute
from vivid.Classes.Relation import Relation
from vivid.Classes.AttributeStructure import AttributeStructure
from vivid.Classes.AttributeSystem import AttributeSystem
from vivid.Classes.RelationSymbol import RelationSymbol
from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.ConstantAssignment import ConstantAssignment
from vivid.Classes.NamedState import NamedState
from vivid.Classes.AttributeInterpretation import AttributeInterpretation
from vivid.Classes.Formula import Formula
from vivid.Classes.AssumptionBase import AssumptionBase
from vivid.Classes.Context import Context

from vivid.Classes.InferenceRules import widening


def test_thinning():
    """Test ."""
    pass


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
        context1 = Context(assumption_base, world)
        context2 = Context(assumption_base, named_state)

        assert widening(context1, named_state)
        assert widening(context1, world)
        assert not widening(context2, world)
        assert widening(context2, named_state)

    test_version_named_state()
    test_context_bound()
    test_context_unbound()


def test_observe():
    """Test ."""
    pass


def test_diagrammatic_absurdity():
    """Test ."""
    pass


def test_sentential_absurdity():
    """Test ."""
    pass


def test_diagram_reiteration():
    """Test ."""
    pass
