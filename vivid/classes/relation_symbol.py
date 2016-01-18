"""relation_symbol module."""


class RelationSymbol(object):
    """
    Relation Symbols class for Vocabularies.

    :ivar name: a ``str`` designating the name of the RelationSymbol object.
    :ivar arity: an ``int`` designating the arity of the RelationSymbol object.
    """

    def __init__(self, name, arity):
        """
        Construct a RelationSymbol object.

        :param name: The name of the RelationSymbol object.
        :type  name: ``str``
        :param arity: The arity of the RelationSymbol object.
        :type  arity: ``int``

        :raises TypeError: ``name`` parameter must be a ``str`` and ``arity`` \
        parameter must be an ``int``\.
        :raises ValueError: ``arity`` must be positive.
        """

        if not isinstance(name, str):
            raise TypeError('name parameter must be of type str')
        if not isinstance(arity, int):
            raise TypeError('arity parameter must be of type int')

        from copy import deepcopy

        if arity <= 0:
            raise ValueError("arity must be a positive integer")

        self._name = deepcopy(name)
        self._arity = deepcopy(arity)
        self._is_RelationSymbol = True

    def __eq__(self, other):
        """
        Determine if two RelationSymbol objects are equal via the ``==``
        operator.
        """

        name_cond = self._name == other._name
        arity_cond = self._arity == other._arity

        if name_cond and arity_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two RelationSymbol objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """
        Deepcopy a RelationSymbol object via the ``copy.deepcopy`` method.
        """

        from copy import deepcopy
        return RelationSymbol(deepcopy(self._name), deepcopy(self._arity))

    def _key(self):
        """
        Private key function for hashing.

        :return: 2-tuple consisting of (``name``, ``arity``)
        :rtype: tuple
        """

        return (self._name, self._arity)

    def __hash__(self):
        """
        Hash implementation for set functionality of RelationSymbol objects.
        """

        return hash(self._key())

    def __str__(self):
        """
        Return a readable string representation of a RelationSymbol object.
        """

        name_str = self._name
        return name_str

    def __repr__(self):
        """Return a string representation of a RelationSymbol object."""
        return self.__str__()
