"""Formula class; imutable."""


class Formula(object):
    """Class for a formula in respect to some Vocabulary sigma."""

    def __init__(self, vocabulary, name, *terms):
        """Construct a Formula object."""

        if not hasattr(vocabulary, "_is_Vocabulary"):
            raise TypeError("vocabulary parameter must be a Vocabulary object")
        if type(name) != str:
            raise TypeError(name + " must be a string")

        relation_symbol_names = [rs._name for rs in vocabulary._R]
        if name not in relation_symbol_names:
            raise ValueError(
                "Name must match some RelationSymbol in Vocabulary")

        if not terms:
            raise ValueError("at least 1 term must be provided")

        C, V = vocabulary._C, vocabulary._V

        for t in terms:

            if t in C:
                in_C = True
            else:
                in_C = False
            if t in V:
                in_V = True
            else:
                in_V = False

            # Vocabulary takes care of ensuring no overlap between C and V
            if not in_C and not in_V:
                raise ValueError(
                    "all terms must be contained in vocabulary's C or V")

        from copy import deepcopy
        self._vocabulary = vocabulary
        self._name = deepcopy(name)
        self._terms = list(terms)
        self._is_Formula = True

    def __eq__(self, other):
        """Implement == operator for Formula."""
        if not hasattr(other, "_is_Formula"):
            raise TypeError(
                "can only compare Formula object with another Formula object")

        vocab_cond = self._vocabulary is other._vocabulary
        name_cond = self._name == other._name
        terms_cond = set(self._terms) == set(other._terms)

        if vocab_cond and name_cond and terms_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != operator for Formula object."""
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Implement + operator for Formula (implicitly creating an
        AssumptionBase).
        """

        from copy import deepcopy
        from AssumptionBase import AssumptionBase

        # Handle adding an AssumptionBase
        if hasattr(other, "_is_AssumptionBase"):
            # Edge cases
            if len(other) == 0:
                if other._vocabulary is not self._vocabulary:
                    raise ValueError(
                        "Cannot add an AssumptionBase's with different "
                        "Vocabulary than this Formula object")
                return AssumptionBase(self)

            for other_formula in other:
                if other_formula._vocabulary is not self._vocabulary:
                    raise ValueError(
                        "Cannot add an AssumptionBase's with different "
                        "Vocabulary than this Formula object")
                if other_formula._name == self._name:
                    raise ValueError("Duplicate Formula objects not permitted")

            return AssumptionBase(*deepcopy(other._formulae + [self]))

        # Handle adding a Formula
        if hasattr(other, "_is_Formula"):
            if other._vocabulary is not self._vocabulary:
                raise ValueError(
                    "Cannot add Formula's with different Vocabulary's")
            if other._name == self._name:
                raise ValueError("Duplicate Formula objects not permitted")

            return AssumptionBase(*deepcopy([self, other]))

        raise TypeError(
            "Only Formula and AssumptionBase objects can be added to an "
            "AssumptionBase")

    def __str__(self):
        """Implement str(Formula)."""
        return self._name + '(' + ', '.join(
            [str(t) for t in self._terms]) + ')'

    def __repr__(self):
        """Implement repr(Formula)."""
        return self.__str__()

    def _key(self):
        """Implement key for hashing Formula."""
        return (hash(self._vocabulary), self._name, tuple(sorted(self._terms)))

    def __hash__(self):
        """Implement hash(Formula)."""
        return hash(self._key())

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for formula object."""
        from copy import deepcopy
        return Formula(self._vocabulary,
                       deepcopy(self._name),
                       *deepcopy(self._terms))

    def assign_truth_value(self, attribute_interpretation, named_state, X):
        """
        Assign truth value in (true, false, unknown} to Formula given an
        arbitrary NamedState and VariableAssignment
        """

        def get_relation_arguments(definition):
            """Return the arguments provided in Relation definition."""

            start_paren = definition.find('(')
            end_paren = definition.find(')')

            arg_string = definition[start_paren + 1:end_paren]
            return arg_string.split(',')

        if not hasattr(attribute_interpretation,
                       "_is_AttributeInterpretation"):
            raise TypeError(
                "attribute_interpretation parameter must an "
                "AttributeInterpretation object")

        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be a NamedState object")

        if not hasattr(X, "_is_VariableAssignment"):
            raise TypeError(
                "X parameter must be a VariableAssignment object")

        if self._vocabulary == attribute_interpretation._vocabulary == \
                named_state._p._vocabulary == X._vocabulary:
            pass
        else:
            raise ValueError(
                "Vocabulry's of Formula, AttributeInterpretation, NamedState, "
                "and VariableAssignment must match")

        # name should always be in interpretation table
        for entry in attribute_interpretation:
            if entry[0]._name == self._name:
                R_I = entry
                break
        else:
            raise ValueError(self._name + " must be in intepretation table")

        p = named_state._p
        profile = list(R_I[3])
        terms = self._terms
        relation = named_state._attribute_system._attribute_structure[
            int(R_I[2][1:])]

        if len(profile) != len(relation._DR):
            raise ValueError(
                "number of profile pairs must be equal to the number "
                "of arguments the relation takes")

        # compiling profile into attribute object pairs that will be
        # substituted into the expression

        # check if each index is valid in respect to list of terms
        # i.e., j_x has corresponding (t^{p,X})_{j_x}
        for index in [pair[1] for pair in profile]:
            if index > len(terms):
                raise ValueError(
                    "each index corresponds to an index in formula's terms "
                    "list; indicies may not exceed the amount of terms")

        profile_copy = [pr for pr in profile]

        # for each pair in profile grab formula term corresponding to the
        # pair's index; shifted down 1 as indexing starts at 0 and not 1 then
        # rewrite that pair with the corresponding term instead of index
        profile = map(lambda pair: (pair[0], terms[pair[1] - 1]), profile)

        # Replace Vocabulary C and V's with their respective objects
        # according to p and X
        for i, pair in enumerate(profile):
            try:
                obj = p._mapping[pair[1]]
            except KeyError:
                try:
                    obj = X._mapping[pair[1]]
                except KeyError:
                    return "unknown"

            profile[i] = (pair[0], obj)

        relation_args = get_relation_arguments(relation._definition)
        worlds = named_state.get_worlds()

        # sort by longest arguments firsts so we can ensure unambiguous
        # replacement when swapping in the valuations associated with the
        # ao_pairs from each world into the relation definition
        relation_args, profile = (
            list(t) for t in zip(*sorted(zip(relation_args, profile),
                                 key=lambda x: len(x[0]),
                                 reverse=True)))

        # we now check the formula against each possible world within the state
        # First, create a ParserSet object so we can attempt parsing of formula
        from Parsers.ParserSet import ParserSet
        parser_set = ParserSet()

        truth_values = []
        for world in worlds:
            # break reference from Relation
            definition = str(relation._definition)
            # zip arguments in Relation and valuations together
            valuations = [
                world._ascriptions[ao_pair] for ao_pair in profile]
            substitutions = zip(relation_args, valuations)

            for substitution in substitutions:
                pattern, valueset = substitution
                # we're swapping in a valuation valueset so just shed
                # the prefix 'V(' and suffix ')'
                value = str(valueset)[2:-1]
                definition = definition.replace(pattern, value)

            # trim the LHS of the definition to make evaluatable expression
            expression = definition[definition.find(" <=> ") + 5:]

            # Try each parser in ParserSet; raise ValueError if no parser
            # can successfully parse formula
            for parser in parser_set:
                try:
                    result = parser(expression)
                    truth_values.append(result)
                    break
                except:
                    pass
            else:
                raise ValueError("Unable to parse formula")

        if all(truth_values):
            return True
        elif not any(truth_values):
            return False
        else:
            return "unknown"

    @staticmethod
    def get_basis(constant_assignment, variable_assignment,
                  attribute_interpretation, *formulae):
        """
        Get the basis of a set of formulae w.r.t. a ConstantAssignment,
        VariableAssignment, and AttributeInterpretation.
        """

        if not formulae:
            raise ValueError("At least one Formula must be provided")

        basis = set([])

        for formula in formulae:

            if not hasattr(formula, "_is_Formula"):
                raise TypeError(
                    "All positional arguments provided in formulae must be "
                    "Formula objects.")

            # name should always be in interpretation table
            for entry in attribute_interpretation:
                if entry[0]._name == formula._name:
                    R_I = entry
                    break
            else:
                raise ValueError(
                    formula._name + " must be in intepretation table")

            profile = list(R_I[3])
            terms = formula._terms

            profile = map(lambda pair: (pair[0], terms[pair[1] - 1]), profile)

            # Replace Vocabulary C and V's with their respective objects
            # according to p and X
            for i, pair in enumerate(profile):
                try:
                    obj = constant_assignment._mapping[pair[1]]
                except KeyError:
                    try:
                        obj = variable_assignment._mapping[pair[1]]
                    except KeyError:
                        raise ValueError("term: " + pair[1] + " undefined")

                profile[i] = (pair[0], obj)

            # Add all ao-pairs in profile to basis if they're not in it already
            basis.update(profile)

        return list(basis)


def main():
    """Quick tests."""
    from Point import Point
    from Relation import Relation
    from Attribute import Attribute
    from AttributeStructure import AttributeStructure
    from RelationSymbol import RelationSymbol
    from Vocabulary import Vocabulary
    from AttributeSystem import AttributeSystem
    from ConstantAssignment import ConstantAssignment
    from NamedState import NamedState
    from VariableAssignment import VariableAssignment
    from AttributeInterpretation import AttributeInterpretation
    from AssumptionBase import AssumptionBase

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
    r_meets = Relation(
        'R5(p, wl1s, wl1e, wl2s, wl2e) <=> meets(p, wl1s, wl1e, wl2s, wl2e)',
        ['point', 'point', 'point', 'point', 'point'], 5)

    attribute_structure = AttributeStructure(
        point, r_is_on, r_not_same_point, r_clocks_unequal, r_can_observe,
        r_meets)

    rs_is_on = RelationSymbol('IS_ON', 3)
    rs_not_same_point = RelationSymbol('NOT_SAME_POINT', 2)
    rs_clocks_unequal = RelationSymbol('CLOCKS_UNEQUAL', 2)
    rs_can_observe = RelationSymbol('CAN_OBSERVE', 4)
    rs_meets = RelationSymbol('MEETS', 5)

    vocabulary = Vocabulary(['P1', 'P2', 'P3', 'P4', 'P5'],
                            [rs_is_on, rs_not_same_point,
                             rs_clocks_unequal, rs_can_observe, rs_meets],
                            [])

    profiles = [
        [rs_is_on, ('point', 1), ('point', 2), ('point', 3)],
        [rs_not_same_point, ('point', 1), ('point', 2)],
        [rs_clocks_unequal, ('point', 1), ('point', 2)],
        [rs_can_observe,
         ('point', 1), ('point', 2), ('point', 3), ('point', 4)],
        [rs_meets,
         ('point', 1), ('point', 2), ('point', 3), ('point', 4), ('point', 5)]]

    mapping = {rs_is_on: 1, rs_not_same_point: 2, rs_clocks_unequal: 3,
               rs_can_observe: 4, rs_meets: 5}

    attribute_interpretation = AttributeInterpretation(vocabulary,
                                                       attribute_structure,
                                                       mapping,
                                                       profiles)

    objects = ['p1', 'p2', 'p3', 'p4', 'p5']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system,
                           {'P1': 'p1', 'P2': 'p2', 'P3': 'p3', 'P4': 'p4',
                            'P5': 'p5'})

    named_state = NamedState(attribute_system, p, {
                             ('point', 'p1'): [Point(1.5, 1.5, 1.5, 1.5)],
                             ('point', 'p2'): [Point(2.0, 2.0, 2.0, 2.0)],
                             ('point', 'p3'): [Point(1.0, 1.0, 1.0, 1.0)],
                             ('point', 'p4'): [Point(3.0, 3.0, 3.0, 3.0)],
                             ('point', 'p5'): [Point(2.0, 2.0, 2.0, 2.0)]})

    f1 = Formula(vocabulary, 'IS_ON', 'P1', 'P3', 'P4')
    f2 = Formula(vocabulary, 'NOT_SAME_POINT', 'P1', 'P2')
    f3 = Formula(vocabulary, 'CLOCKS_UNEQUAL', 'P1', 'P2')
    f4 = Formula(vocabulary, 'CAN_OBSERVE', 'P1', 'P2', 'P3', 'P4')
    f5 = Formula(vocabulary, 'MEETS', 'P1', 'P2', 'P3', 'P4', 'P5')

    VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)

    assumption_base = AssumptionBase(f1, f2, f3, f4)

    print Formula.get_basis(
        named_state._p, VA, attribute_interpretation, f1, f2, f3, f4)

    # for f in assumption_base:
    #    print f.assign_truth_value(attribute_interpretation, named_state, VA)

    named_state.set_ascription(('point', 'p4'), [Point(1.0, 1.0, 1.0, 1.0)])
    # print f5.assign_truth_value(attribute_interpretation, named_state, VA)

if __name__ == "__main__":
    main()
