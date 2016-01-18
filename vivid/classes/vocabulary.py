"""vocabulary module."""


class Vocabulary(object):
    """
    First-Order Vocabulary class.

    :ivar C: The constants of the vocabulary.
    :ivar R: The relation symbols of the vocabulary.
    :ivar V: the variables of the vocabulary.
    """

    def __init__(self, C, R, V):
        """
        Construct a Vocabulary object. Each parameter ``C``, ``R`` and ``V``
        are sorted before being stored.

        :param C: The constants of the Vocabulary object; held as a ``list`` \
        of ``str``\s.
        :type  C: ``list``
        :param R: The relation symbols of the Vocabulary object; held as a  \
        ``list`` of RelationSymbol objects.
        :type  R: ``list``
        :param V: The variables of the Vocabulary object; held as a ``list`` \
        of ``str``\s.
        :type  V: ``list``

        :raises TypeError: ``C``, ``R``, and ``V`` parameters must all be \
        lists, ``C`` and ``V`` must be contain only ``str``\s and ``R`` must \
        contain only RelationSymbol objects.
        :raises ValueError: ``C`` and ``V`` cannot overlap and duplicates are \
        not permitted in any of the lists.
        """

        if not isinstance(C, list):
            raise TypeError('C parameter must be of type list')
        if not isinstance(R, list):
            raise TypeError('R parameter must be of type list')
        if not isinstance(V, list):
            raise TypeError('V parameter must be of type list')

        for c in C:
            if not isinstance(c, str):
                raise TypeError(
                    'all entries in C parameter must be of type str')

        for rs in R:
            if not hasattr(rs, "_is_RelationSymbol"):
                raise TypeError(
                    'all entries in R parameter must be of type RelationSymbol')

        for v in V:
            if not isinstance(v, str):
                raise TypeError(
                    'all entries in V parameter must be of type str')

        intersection = (set(C) & set(V))
        if len(intersection) > 0:
            raise ValueError(
                'C and V parameters may not have a common element')

        if len(C) != len(set(C)):
            raise ValueError("Duplicate constants not permitted")

        names = [rs._name for rs in R]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate RelationSymbol names not permitted")

        if len(V) != len(set(V)):
            raise ValueError("Duplicate variables not permitted")

        self._C = sorted(list(set(C)), key=lambda c: c.lower())
        self._R = sorted(list(set(R)), key=lambda rs: rs._name.lower())
        self._V = sorted(list(set(V)), key=lambda v: v.lower())
        self._is_Vocabulary = True

    def __eq__(self, other):
        """
        Determine if two Vocabulary objects are equal via ``==`` operator.
        """

        # constructor removes duplicates, so set comparison okay
        c_cond = set(self._C) == set(other._C)
        r_cond = set(self._R) == set(other._R)
        v_cond = set(self._V) == set(other._V)

        if c_cond and r_cond and v_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two Vocabulary objects are not equal via ``!=`` operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy a Vocabulary object via the ``copy.deepcopy`` method.
        """

        from copy import deepcopy
        return Vocabulary(
            deepcopy(self._C), deepcopy(self._R), deepcopy(self._V))

    def __contains__(self, key):
        """
        Determine if a Vocabulary contains the ``str`` or RelationSymbol object
        in ``key`` parameter.

        :param key: The ``str`` or RelationSymbol object to test for \
        membership in this Vocabulary.
        :type  key: RelationSymbol|str
        """

        if hasattr(key, "_is_RelationSymbol"):
            return key in self._R

        return key in self._C or key in self._V

    def add_constant(self, constant):
        """
        Add a constant to this Vocabulary object's ``C``.

        :param constant: the new constant to add to the Vocabulary's ``C``\.
        :type  constant: str

        :raises TypeError: ``constant parameter must be a ``str``\.
        :raises ValueError: duplicate symbols are not permitted.
        """

        if type(constant) != str:
            raise TypeError("constant parameter must be a string")

        in_C = constant in self._C
        in_V = constant in self._V
        if not in_C and not in_V:
            self._C = sorted(self._C + [constant], key=lambda c: c.lower())
        else:
            raise ValueError("duplicate symbol cannot be added")

    def add_variable(self, variable):
        """
        Add a constant to this Vocabulary object's ``V``.

        :param variable: the new variable to add to the Vocabulary's ``V``\.
        :type  variable: str

        :raises TypeError: ``variable parameter must be a ``str``\.
        :raises ValueError: duplicate symbols are not permitted.
        """

        if type(variable) != str:
            raise TypeError("variable parameter must be a string")

        in_C = variable in self._C
        in_V = variable in self._V
        if not in_C and not in_V:
            self._V = sorted(self._V + [variable], key=lambda v: v.lower())
        else:
            raise ValueError("duplicate symbol cannot be added")

    def __str__(self):
        """Return a readable string representation of a Vocabulary object."""
        c_str = '[' + ''.join([c + ', ' for c in self._C])[:-2] + ']'
        r_str = '[' + ''.join([str(r) + ', ' for r in self._R])[:-2] + ']'
        v_str = '[' + ''.join([v + ', ' for v in self._V])[:-2] + ']'

        return '(' + c_str + ', ' + r_str + ', ' + v_str + ')'

    def __repr__(self):
        """Return a string representation of a Vocabulary object."""
        return self.__str__()

    def _key(self):
        """
        Private key function for hashing.

        :return: 3-tuple consisting of (``C``, ``R``, ``V``)
        :rtype: tuple
        """

        return (tuple(self._C), tuple(self._R), tuple(self._V))

    def __hash__(self):
        """
        Hash implementation for set functionality of Vocabulary objects.
        """

        return hash(self._key())


def main():
    """short tests."""
    pass

if __name__ == "__main__":
    main()
