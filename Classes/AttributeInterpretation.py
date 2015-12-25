"""Attribute Interpretation object."""

from Vocabulary import Vocabulary
from RelationSymbol import RelationSymbol
from AttributeStructure import Attribute, Relation, AttributeStructure


class AttributeInterpretation(object):
    """AttributeInterpretation class to build an interpretation table."""

    def __init__(self, vocabulary, attribute_structure, mapping, profiles):
        """Construct an AttributeInterpretation object."""
        if not hasattr(vocabulary, "_is_Vocabulary"):
            raise TypeError("vocabulary parameter must be a Vocabulary object")
        if not hasattr(attribute_structure, "_is_AttributeStructure"):
            raise TypeError(
                "attribute_structure parameter must be an "
                "AttributeStructure object")
        if type(mapping) != dict:
            raise TypeError(
                "mapping parameter must be dictionary of RelationSymbol's to "
                "Relations denoted by subscript")
        if type(profiles) != list:
            raise TypeError("profiles parameter must be list")

        source, target = mapping.keys(), mapping.values()

        if not all(hasattr(i, "_is_RelationSymbol") for i in source):
            raise ValueError(
                "All keys provided to mapping parameter must be "
                "RelationSymbol objects")

        if not all(type(i) == int for i in target):
            raise ValueError(
                "All values provided to mapping parameter must be integer "
                "subscripts")

        valid_subscripts = attribute_structure._relations.keys()
        valid_r_symbols = vocabulary._R
        profile_r_symbols = [prof[0] for prof in profiles]

        if len(profile_r_symbols) != len(set(profile_r_symbols)):
            raise ValueError(
                "Duplicate profiles not permitted.")

        # only need to do this for subscripts; dictionaries can't have
        # duplicate keys
        if len(target) != len(set(target)):
            raise ValueError(
                "Duplicate subscripts; Mapping must be 1-to-1")

        # Ensure source and target elements are valid
        if not set(source) == set(valid_r_symbols) == set(profile_r_symbols):
            raise ValueError(
                "The set of RelationSymbol's provided in mapping and the set "
                "of RelationSymbol's in Vocabulary and the set of "
                "RelationSymbol's provided in profile must all be equal")

        if not set(target) <= set(valid_subscripts):
            raise ValueError(
                "All subscripts provided in mapping must be subscripts of "
                "Relation's in AttributeStructure")

        interpretation_table = []

        valid_labels = attribute_structure.get_labels()
        for profile in profiles:
            # split profile
            R, prof = profile[0], profile[1:]

            # extract relevant fields
            n = R._arity
            R_prime_subscript = mapping[R]
            for relation in attribute_structure._relations.values():
                if relation._subscript == R_prime_subscript:
                    R_prime = relation

            labels = [pair[0] for pair in prof]
            j_x = [pair[1] for pair in prof]

            # ensure all labels in profile exist in AttributeStructure
            if not set(labels) <= set(valid_labels):
                raise ValueError(
                    "Invalid label provided in profile: " + str(profile))

            # Ensure 1 <= j_x <= n for all j_x in profile where n is the
            # RelationSymbol's arity
            if not all([1 <= j_i <= n for j_i in j_x]):
                raise ValueError(
                    "1 <= j_x <= n must be true for all j_x in profile")

            entry = [R, R_prime.get_arity(),
                     'R' + str(R_prime._subscript),
                     prof]
            interpretation_table.append(entry)

        # Save copy of all params for deepcopy implementation
        from copy import deepcopy
        self._vocabulary = vocabulary
        self._attribute_structure = deepcopy(attribute_structure)
        self._mapping = deepcopy(mapping)
        self._profiles = deepcopy(profiles)

        self._table = interpretation_table
        self._relation_symbols = [e[0] for e in interpretation_table]
        self._is_AttributeInterpretation = True

    def __eq__(self, other):
        """Implement == operator for AttributeInterpretation."""
        if not hasattr(other, "_is_AttributeInterpretation"):
            raise TypeError(
                "Can only compare an AttributeInterpretation object with "
                "another AttributeInterpretation object")

        # No duplicates so just checking set equality works
        if self._attribute_structure != other._attribute_structure:
            return False

        if self._vocabulary != other._vocabulary:
            return False

        rs_cond = set(self._relation_symbols) == set(other._relation_symbols)
        if not rs_cond:
            return False

        # easy look up table to determine if set of rows are equal
        self_dict = {entry[0]: entry[1:] for entry in self._table}
        other_dict = {entry[0]: entry[1:] for entry in other._table}

        # for every row, compare
        for key in self_dict.keys():
            # Pull the rows from the lookup table
            self_row = self_dict[key]
            other_row = other_dict[key]

            arity_cond = self_row[0] == other_row[0]
            r_cond = self_row[1] == other_row[1]
            profile_cond = self_row[2] == other_row[2]

            # if some pair of entries on the rows are unequal,
            # AttributeInterpretation's are not equal
            if not arity_cond or not r_cond or not profile_cond:
                return False

        return True

    def __ne__(self, other):
        """Implement == operator for AttributeInterpretation."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for AttributeInterpretation object."""
        from copy import deepcopy
        return AttributeInterpretation(
            deepcopy(self._vocabulary),
            self._attribute_structure,
            self._mapping,
            self._profiles)

    def __iter__(self):
        """Implement iterator for AttributeInterpretation."""
        for entry in self._table:
            yield entry

    def __str__(self):
        """Implement str(AttributeInterpretation)."""
        return '\n'.join([str(entry) for entry in self._table])

    def __repr__(self):
        """Implement repr(AttributeInterpretation)."""
        return '\n'.join([str(entry) for entry in self._table])


def main():
    """Quick tests."""

    a = Attribute('hour', ['0,...,23'])
    a2 = Attribute('minute', ['0,...,59'])
    r_ahead = Relation('R1(h1,m1,h2,m2) <=> h1 > h2 or (h1 = h2 and m1 > m2)',
                       ['hour', 'minute', 'hour', 'minute'], 1)
    r_behind = Relation('R2(h1,m1,h2,m2) <=> h1 < h2 or (h1 = h2 and m1 < m2)',
                        ['hour', 'minute', 'hour', 'minute'], 2)
    r_pm = Relation('R3(h1) <=> h1 > 12', ['hour'], 3)
    r_am = Relation('R4(h1) <=> h1 < 12', ['hour'], 4)
    attribute_structure = AttributeStructure(
        a, a2, r_ahead, r_behind, r_pm, r_am)

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    profiles = [
        [ahead_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [behind_rs, ('hour', 1), ('minute', 1), ('hour', 2), ('minute', 2)],
        [pm_rs, ('hour', 1)]
    ]

    mapping = {ahead_rs: 1, behind_rs: 2, pm_rs: 3}

    ai = AttributeInterpretation(
        vocabulary, attribute_structure, mapping, profiles)
    print ai == ai

if __name__ == "__main__":
    main()
