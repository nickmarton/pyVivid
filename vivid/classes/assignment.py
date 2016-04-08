"""This section introduces the Assignment class."""


class Assignment(object):
    """
    Assignment class. The Assignment class functions as a superclass for the
    ConstantAssignment and VariableAssignment classes.

    :ivar vocabulary: A reference to the Vocabulary object :math:`\Sigma` \
    that the Assignment is defined over.
    :ivar attribute_system: A copy of the AttributeSystem the Assignment \
    originates from.
    :ivar _is_Assignment: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self, vocabulary, attribute_system):
        """
        Construct a base Assignment.

        :param vocabulary: The Vocabulary :math:`\Sigma` the Assignment is \
        defined over.
        :type  vocabulary: Vocabulary
        :param attribute_system: The AttributeSystem from which the objects \
        in the Assignment come from.
        :type  attribute_system: AttributeSystem

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object and ``attribute_system`` parameter must be an AttributeSystem \
        object.
        """

        from copy import deepcopy

        if not hasattr(vocabulary, "_is_Vocabulary"):
            raise TypeError(
                "vocabulary parameter must be of type Vocabulary")

        if not hasattr(attribute_system, "_is_AttributeSystem"):
            raise TypeError(
                "attribute_system parameter must be of type AttributeSystem")

        self._vocabulary = vocabulary
        self._attribute_system = deepcopy(attribute_system)
        self._is_Assignment = True

    def __eq__(self, other):
        """
        Determine if two Assignment objects are equal via the ``==`` operator.
        """

        vocabulary_cond = self._vocabulary == other._vocabulary
        objects_cond = self._attribute_system._objects == \
            other._attribute_system._objects

        if vocabulary_cond and objects_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two Assignment objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)
