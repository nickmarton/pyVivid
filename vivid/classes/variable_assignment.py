"""variable_assignment module."""

from assignment import Assignment


class VariableAssignment(Assignment):
    """
    VariableAssignment class. A VariableAssignment is a total
    function :math:`\chi` from the variables V of some Vocabulary to the
    objects {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`} of some AttributeSystem.

    :ivar vocabulary: a reference to the Vocabulary object the \
    VariableAssignment is defined over.
    :ivar attribute_system: a copy of the AttributeSystem the \
    VariableAssignment originates from.
    :ivar mapping: The mapping V :math:`\longrightarrow` \
    {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`}
    :ivar source: The variable used in the total mapping :math:`\chi`.
    :ivar target: The objects used in the total mapping :math:`\chi`.
    :ivar _is_VariableAssignment: An identifier to use in place of type or \
    isinstance.
    """

    def __init__(self, vocabulary, attribute_system, mapping, dummy=False):
        """
        Construct a VariableAssignment object.

        :param vocabulary: The Vocabulary the VariableAssignment is defined over.
        :type  vocabulary: Vocabulary
        :param attribute_system: The AttributeSystem from which the objects \
        in the Assignment come from.
        :type  attribute_system: AttributeSystem
        :param mapping: The mapping :math:`\chi` from the variables V of \
        ``vocabulary`` to the objects \
        {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`} of ``attribute_system``.
        :type  mapping: ``dict``
        :param dummy: A flag for creating a dummy (i.e., empty) \
        VariableAssignment object.
        :type  dummy: ``bool``

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object, ``attribute_system`` parameter must be an AttributeSystem \
        object and ``mapping`` parameter must be a ``dict`` with ``str`` keys \
        and values.
        :raises ValueError: all keys in ``mapping`` parameter must be in \
        ``vocabulary`` parameter's variables and all values in ``mapping`` \
        parameter must be unique and match some object in \
        ``attribute_system`` parameter and variables must span all of V \
        (unless dummy flag is on).
        """

        if not isinstance(mapping, dict):
            raise TypeError(
                "mapping parameter must be of type dict")

        if not all([isinstance(s, str) for s in mapping.keys()]):
            raise TypeError("mapping must be of form str: str")

        if not all([isinstance(s, str) for s in mapping.values()]):
            raise TypeError("mapping must be of form str: str")

        if dummy:
            Assignment.__init__(self, vocabulary, attribute_system)
            self._mapping = {}
            self._is_VariableAssignment = True
        else:
            source = mapping.keys()
            target = mapping.values()

            if len(source) != len(set(source)) or len(target) != len(set(target)):
                raise ValueError(
                    "duplicate values in mapping parameter "
                    "are not allowed; mapping must be 1-to-1.")

            # total mapping so check for equality
            source_condition = set(source) <= set(vocabulary._V)

            target_condition = set(target) <= set(attribute_system._objects)

            if source_condition and target_condition:
                Assignment.__init__(self, vocabulary, attribute_system)
                self._mapping = mapping
                self._source = mapping.keys()
                self._target = mapping.values()
                self._is_VariableAssignment = True
            else:
                raise ValueError(
                    "VariableAssignment must be a function from "
                    "vocabulary._V to attribute_system._objects")

    def __eq__(self, other):
        """
        Determine if two VariableAssignment objects are equal via the ``==`` \
        operator.
        """

        vocabulary_cond = self._vocabulary == other._vocabulary
        asys_cond = self._attribute_system == other._attribute_system
        mapping_cond = self._mapping == other._mapping

        if vocabulary_cond and asys_cond and mapping_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two VariableAssignment objects are not equal via the
        ``!=`` operator.
        """
        return not self.__eq__(other)

    def __getitem__(self, key):
        """
        Retrive the object mapped to the constant given by ``key`` parameter
        via indexing (e.g. ``VariableAssignment[key]``).

        :param key: The variable to use for retrieval.
        :type  key: str

        :raises KeyError: variable given by ``key`` parameter is not in this \
        VariableAssignment's ``source``.
        :raises TypeError: ``key`` parameter must be a ``str``.
        """

        if not isinstance(key, str):
            raise TypeError("key parameter must be of type string")

        try:
            return self._mapping[key]
        except KeyError:
            raise KeyError(str(key) + " is not in source")

    def __deepcopy__(self, memo):
        """
        Deepcopy a ConstantAssignment object via the ``copy.deepcopy`` method.
        This does not break the reference to ``vocabulary`` member.
        """

        from copy import deepcopy

        return VariableAssignment(
            self._vocabulary,
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def __str__(self):
        """
        Return a readable string representation of a VariableAssignment object.
        """

        return 'VA' + str(self._mapping)

    def __repr__(self):
        """Return a string representation of a VariableAssignment object."""
        return self.__str__()
