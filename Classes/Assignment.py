"""Assignment base class."""

from vivid.Classes.Vocabulary import Vocabulary
from vivid.Classes.AttributeSystem import AttributeSystem

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

        from copy import deepcopy

        if not hasattr(vocabulary, "_is_Vocabulary"):
            raise TypeError(
                "vocabulary parameter must be of type Vocabulary")

        if not hasattr(attribute_system, "_is_AttributeSystem"):
            raise TypeError(
                "attribute_system parameter must be of type AttributeSystem")

        self._vocabulary = deepcopy(vocabulary)
        self._attribute_system = deepcopy(attribute_system)
        self._is_Assignment = True

    def __eq__(self, other):
        """Implement == for Assignment object."""
        vocabulary_cond = self._vocabulary == other._vocabulary
        objects_cond = self._attribute_system._objects == \
                                            other._attribute_system._objects

        if vocabulary_cond and objects_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != for Assignment object."""
        return not self.__eq__(other)
