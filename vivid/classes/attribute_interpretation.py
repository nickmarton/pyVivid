"""attribute_interpretation module."""

from vocabulary import Vocabulary
from relation_symbol import RelationSymbol
from attribute import Attribute
from relation import Relation
from attribute_structure import AttributeStructure


class AttributeInterpretation(object):
    """
    AttributeInterpretation class.
    Build an interpretation table; that is, a mapping :math:`I` that assigns,
    to each RelationSymbol object of a Vocabulary object :math:`\Sigma`,
    :math:`R \in` R of arity :math:`n`:

    1. a relation :math:`R^{I} \in \mathcal{R}` of some arity *m*, called the
    **realization** of *R*:

    .. centered:: :math:`R^{I} \subset A_{i_{1}} \\times \cdots \\times A_{i_{m}}`
    (where we might have :math:`m \\ne n`); and


    2. a list of *m* pairs
    \ 

    .. centered:: :math:`[(l_{i_{1}}; j_{1}) \cdots (l_{i_{m}}; j_{m})]`
    called the **profile** of *R* and denoted by :math:`Prof(R)`, with
    :math:`1 \le j_{x} \le n` for :math:`x = 1, \ldots, m`

    :ivar vocabulary: The Vocabulary object :math:`\Sigma` of the \
    interpretation.
    :ivar attribute_structure: The AttributeStructure object the \
    interpretation is into.
    :ivar mapping: The mapping R :math:`\\rightarrow \mathcal{R}`.
    :ivar profiles: A list of profiles :math:`[(l_{i_{1}}; j_{1}) \cdots \
    (l_{i_{m}}; j_{m})]`; one for each realization.
    :ivar table: The interpretation table of the attribute interpretation.
    :ivar relation_symbols: A copy of the RelationSymbol objects from \
    :math:`\Sigma` (for convenient access).
    :ivar is_AttributeInterpretation: An identifier to use in place of \
    ``type`` or ``isinstance``.
    """

    def __init__(self, vocabulary, attribute_structure, mapping, profiles):
        """
        Construct an AttributeInterpretation object.

        :param vocabulary: The Vocabulary object :math:`\Sigma` to define the \
        AttributeInterpretation over.
        :type  vocabulary: Vocabulary
        :param attribute_structure: The AttributeStructure object for which \
        to define the AttributeInterpretation into.
        :type  attribute_structure: AttributeStructure
        :param mapping: The mapping from the RelationSymbol objects of the \
        Vocabulary object :math:`\Sigma` in the ``vocabulary`` parameter to \
        the Relation objects of the AttributeStructure object in the \
        ``attribute_structure`` parameter; the keys being RelationSymbol \
        objects and values being ``int``\s corresponding to the subscripts of \
        the AttributeStructure Relation objects.
        :type  mapping: ``dict``
        :param profiles: A list of realizations corresponding to the mapping \
        wherein each element is a list where the first element is the \
        RelationSymbol and the following elements are 2-tuples \
        :math:`(l_{i_{k}}; j_{k})`.
        :type  profiles: ``list``

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object, ``attribute_structure`` parameter must be an \
        AttributeStructure object, ``mapping`` parameter myst be a ``dict`` \
        and ``profile`` parameter must be a ``list``.
        :raises ValueError: All keys in the ``mapping`` parameter must be \
        RelationSymbol objects and all values must be unique ``int``\s, \
        duplicate profiles are not permitted (determined by repeated \
        RelationSymbol objects), the set of RelationSymbol's provided in \
        the ``mapping`` parameter and the set of RelationSymbol's in the \
        ``vocabulary`` parameter and the set of RelationSymbol's provided in \
        the ``profile`` parameter must all be equal, all subscripts provided \
        in the ``mapping`` parameter keys must be valid subscripts of \
        Relation objects in the ``attribute_structure`` parameter, all \
        :math:`l_{i_{k}}` in :math:`(l_{i_{k}}; j_{k})` 2-tuples provided in \
        each realization of the ``profile`` parameter must be a label of some \
        Attribute object in the ``attribute_structure`` parameter, and all \
        :math:`j_{k}` in :math:`(l_{i_{k}}; j_{k})` 2-tuples provided in each \
        realization of the ``profile`` parameter must be between 1 and the \
        arity of the RelationSymbol object of the realization.
        """

        if not hasattr(vocabulary, "_is_Vocabulary"):
            raise TypeError("vocabulary parameter must be a Vocabulary object")
        if not hasattr(attribute_structure, "_is_AttributeStructure"):
            raise TypeError(
                "attribute_structure parameter must be an "
                "AttributeStructure object")
        if type(mapping) is not dict:
            raise TypeError(
                "mapping parameter must be dictionary of RelationSymbol's to "
                "Relations denoted by subscript")
        if type(profiles) is not list:
            raise TypeError("profiles parameter must be list")

        source, target = mapping.keys(), mapping.values()

        if not all(hasattr(i, "_is_RelationSymbol") for i in source):
            raise ValueError(
                "All keys provided to mapping parameter must be "
                "RelationSymbol objects")

        if not all(type(i) is int for i in target):
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

            entry = [
                R, R_prime.get_arity(), 'R' + str(R_prime._subscript), prof]
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
        """
        Determine if two AttributeInterpretation objects are equal via the
        ``==`` operator.
        """

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
        """
        Determine if two AttributeInterpretation objects are not equal via the
        ``!=`` operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy an AttributeInterpretation object via the ``copy.deepcopy``
        method. This does not break the reference to the underlying Vocabulary
        object :math:`\Sigma`.
        """

        return AttributeInterpretation(
            self._vocabulary,
            self._attribute_structure,
            self._mapping,
            self._profiles)

    def __iter__(self):
        """
        Provide an iterator for the interpretation table of
        AttributeInterpretation objects.

        (e.g. \"``for entry in attribute_interpretation:``\")
        """

        for entry in self._table:
            yield entry

    def __str__(self):
        """
        Return a readable string representation of the AttributeInterpretation
        object.
        """

        return '\n'.join([str(entry) for entry in self._table])

    def __repr__(self):
        """
        Return a string representation of the AttributeInterpretation object.
        """

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
