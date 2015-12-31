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

        ordered_set_terms = []
        for t in terms:
            if t not in ordered_set_terms:
                ordered_set_terms.append(t)

        from copy import deepcopy
        self._vocabulary = deepcopy(vocabulary)
        self._name = deepcopy(name)
        self._terms = ordered_set_terms
        self._is_Formula = True

    def __eq__(self, other):
        """Implement == operator for Formula."""
        if not hasattr(other, "_is_Formula"):
            raise TypeError(
                "can only compare Formula object with another Formula object")

        vocab_cond = self._vocabulary == other._vocabulary
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
                return AssumptionBase(self)

            for other_formula in other:
                if other_formula._vocabulary != self._vocabulary:
                    raise ValueError(
                        "Cannot add an AssumptionBase's with different "
                        "Vocabulary than this Formula object")
                if other_formula._name == self._name:
                    raise ValueError("Duplicate Formula objects not permitted")

            return AssumptionBase(*deepcopy(other._formulae + [self]))

        # Handle adding a Formula
        if hasattr(other, "_is_Formula"):
            if other._vocabulary != self._vocabulary:
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
        return Formula(deepcopy(self._vocabulary),
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

        def handle_is_on_line(profile):
            """
            Get truth value of expressions containing within operator.
            """

            def validate_is_on_line_profile(profile):
                """
                Raise a ValueError if ascriptions form profile don't
                correspond to a Point and line segment.
                """

                ascriptions = [
                    named_state.get_ascription(tup) for tup in profile]

                if len(ascriptions) != 2:
                    raise ValueError(
                        "profile for is_on_line must contain "
                        "exactly two pairs")

                if len(ascriptions[0]) != 1:
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                if not isinstance(ascriptions[0][0], Point):
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                if len(ascriptions[1]) != 2:
                    raise ValueError(
                        "ascription of second profile pair for" +
                        " is_on_line must contain exactly two Points")

                if not isinstance(ascriptions[1][0], Point) or not isinstance(ascriptions[1][1], Point):
                    raise ValueError(
                        "ascription of first profile pair for" +
                        " is_on_line must contain exactly one Point")

                return ascriptions

            def is_on(ascriptions):
                "Return true iff point c intersects the line segment from a to b."
                #  (or the degenerate case that all 3 points are coincident)

                ax, ay = ascriptions[1][0].get_coordinate()
                bx, by = ascriptions[1][1].get_coordinate()
                cx, cy = ascriptions[0][0].get_coordinate()

                return (collinear(ax, ay, bx, by, cx, cy)
                        and (within(ax, cx, bx) if ax != bx else
                             within(ay, cy, by)))

            def collinear(ax, ay, bx, by, cx, cy):
                "Return true iff a, b, and c all lie on the same line."
                return (bx - ax) * (cy - ay) == (cx - ax) * (by - ay)

            def within(p, q, r):
                "Return true iff q is between p and r (inclusive)."
                return p <= q <= r or r <= q <= p

            ascriptions = validate_is_on_line_profile(profile)
            # print "@@@" + str(ascriptions)
            return is_on(ascriptions)

        def handle_through_worldline(profile):
            """
            Handle Relations with definition in the following form:
            R2(p1,p2,l) <=> p1 = p2 through_worldline l
            where p1 and p2 are Points and l is a line segment represented
            by a 2-tuple of Points
            """

            # Create subprofiles to check if points are on line
            p1_on_l_profile = [profile[0], profile[2]]
            p2_on_l_profile = [profile[1], profile[2]]

            p1_on_l = handle_is_on_line(p1_on_l_profile)
            p2_on_l = handle_is_on_line(p2_on_l_profile)

            # if they're both on the same worldine, then observes holds
            both_on_same_worldline = p1_on_l and p2_on_l

            # Get the point objects for comparison
            ascriptions = [named_state.get_ascription(tup) for tup in profile]            # get value set for each object
            p1 = ascriptions[0]
            p2 = ascriptions[1]
            '''
            print "-"*40
            print ascriptions
            print p1 == p2
            print both_on_same_worldline
            print "-"*40
            print
            '''
            # if the p1 and p2 are the same location or both on the same worldline,
            # then p1 and p2 are observable from one another
            if p1 == p2 or both_on_same_worldline:
                return True
            else:
                return False

        def handle_meets(profile):
            """
            Determine if spacetime_position at profile[0] is on both worldlines
            m1 and m2 and therefore if m1 and m2 intersect at sp.
            """

            profile_1 = [profile[0], profile[1]]
            profile_2 = [profile[0], profile[2]]

            sp_on_m1 = handle_is_on_line(profile_1)
            sp_on_m2 = handle_is_on_line(profile_2)

            if sp_on_m1 and sp_on_m2:
                return True
            else:
                return False

        def handle_not_same_point(profile):
            """Handle when two points are being compared for inequality."""

            ascriptions = [named_state.get_ascription(tup) for tup in profile]

            if len(ascriptions) != 2:
                raise ValueError(
                    "only 2 points may be compared")

            if not isinstance(ascriptions[0][0], Point) or not isinstance(ascriptions[1][0], Point):
                raise TypeError(
                    "ascriptions must be of type Point")
            
            p1 = ascriptions[0][0]
            p2 = ascriptions[1][0]

            return p1 != p2

        def handle_clocks_unequal(profile):
            """
            Handle when we compare two spacetime clocks.

            clocks refers to 2nd element in spacetime_position tuple.
            """

            ascriptions = [named_state.get_ascription(tup) for tup in profile]

            if len(ascriptions) != 2:
                raise ValueError(
                    "only 2 points may be compared")

            if not isinstance(ascriptions[0][0], Point) or not isinstance(ascriptions[1][0], Point):
                raise TypeError(
                    "ascriptions must be of type Point")

            p1 = ascriptions[0][0]
            p2 = ascriptions[1][0]

            return p1._coordinate[1] != p2._coordinate[1]

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
        if 'is_on_line' in relation._definition and 'and' in relation._definition:
            return handle_meets(profile)
        elif 'is_on_line' in relation._definition:
            return handle_is_on_line(profile)
        elif 'through_worldline' in relation._definition:
            return handle_through_worldline(profile)
        elif 'not_same_point' in relation._definition:
            return handle_not_same_point(profile)
        elif 'clocks_unequal' in relation._definition:
            return handle_clocks_unequal(profile)
        else:
            # Create a ParserSet object so we can attempt parsing of formula
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

                # trim the LHS of the definition to create evaluatable expression
                expression = definition[definition.find(" <=> ") + 5:]

                print expression
                # return

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

    point = Attribute('point', [Point('x', 'x')])
    relation_2d = Relation('R1(h1) <=> #is_2d(h1)#', ['point'], 1)
    attribute_structure = AttributeStructure(point, relation_2d)
    relation_symbol_2d = RelationSymbol('2D', 1)
    vocabulary = Vocabulary(['P'], [relation_symbol_2d], [])

    profiles = [[relation_symbol_2d, ('point', 1)]]
    mapping = {relation_symbol_2d: 1}

    attribute_interpretation = AttributeInterpretation(vocabulary,
                                                       attribute_structure,
                                                       mapping,
                                                       profiles)

    objects = ['p1']
    attribute_system = AttributeSystem(attribute_structure, objects)
    p = ConstantAssignment(vocabulary, attribute_system, {'P': 'p1'})

    named_state = NamedState(attribute_system, p, {})

    f = Formula(vocabulary, '2D', 'P')

    VA = VariableAssignment(vocabulary, attribute_system, {}, dummy=True)
    f.assign_truth_value(attribute_interpretation, named_state, VA)

if __name__ == "__main__":
    main()
