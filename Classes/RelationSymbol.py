"""Relation Symbol class."""


class RelationSymbol(object):
    """
    Class for Relation Symbols consisting of a name and an arity;

    this class is intended to be a helper class for Vocabulary as later
    on airty is required in addition to a name of a relation in Vocabulary

    name: a string designating the name of the relation symbol.
    arity: an integer designating the arity of the relation symbol.
    """

    def __init__(self, name, arity):
        """Initialize a RelationSymbol object with name and arity."""

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
        """Implement == operator for RelationSymbol object."""
        name_cond = self._name == other._name
        arity_cond = self._arity == other._arity

        if name_cond and arity_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != operator for RelationSymbol object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for RelationSymbol object."""
        from copy import deepcopy
        return RelationSymbol(deepcopy(self._name), deepcopy(self._arity))

    def _key(self):
        """Tuple key for hash function."""
        return (self._name, self._arity)

    def __hash__(self):
        """Hash so sets can use RelationSymbol's."""
        return hash(self._key())

    def __str__(self):
        """Implement str(RelationSymbol)."""
        name_str = self._name
        return name_str

    def __repr__(self):
        """Implement str(RelationSymbol)."""
        return self.__str__()
