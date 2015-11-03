"""Assignment base class."""

class Assignment(object):
    """This is a superclass for generic assignments."""

    def __init__(self, vocabulary, attribute_system):
        """
        Initialize a base Assignment with a mapping from some
        vocabulary to a set of objects while keeping a copy of the
        vocabulary and objects themselves.

        Raise TypeError if vocabulary parameter is not of type Vocabulary,
        or attribute_system parameter is not of type AttributeSystem.
        """

        if not isinstance(vocabulary, Vocabulary):
            raise TypeError(
                "vocabulary parameter must be of type Vocabulary")

        if not isinstance(attribute_system, AttributeSystem):
            raise TypeError(
                "attribute_system parameter must be of type AttributeSystem")

        self._vocabulary = vocabulary
        self._attribute_system = attribute_system
        self._is_Assignment = True

    def __eq__(self, other):
        """Implement == for Assignment object."""
        vocabulary_cond = self._vocabulary == other._vocabulary
        objects_cond = self.attribute_system._objects == \
                                                other.attribute_system._objects

        if vocabulary_cond and objects_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != for Assignment object."""
        return not self.__eq__(other)
