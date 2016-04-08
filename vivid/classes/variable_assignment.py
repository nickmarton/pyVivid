"""This section introduces the VariableAssignment class."""

from assignment import Assignment


class VariableAssignment(Assignment):
    """
    VariableAssignment class. A VariableAssignment is a total
    function :math:`\chi` from the variables V of some Vocabulary object
    :math:`\Sigma`, to the objects :math:`\{s_{1}, \ldots, s_{n}\}` of some
    AttributeSystem :math:`\mathcal{S}`.

    :ivar vocabulary: A reference to the Vocabulary object :math:`\Sigma` the \
    ConstantAssignment is defined over.
    :ivar attribute_system: A copy of the AttributeSystem object \
    :math:`\mathcal{S}` the ConstantAssignment originates from.
    :ivar mapping: The mapping V \
    :math:`\longrightarrow \{s_{1}, \ldots, s_{n}\}`.
    :ivar source: The variables of :math:`\Sigma` used in the total mapping \
    :math:`\chi`.
    :ivar target: The objects of :math:`\mathcal{S}` used in the total \
    mapping :math:`\chi`.
    :ivar _is_VariableAssignment: An identifier to use in place of type or \
    isinstance.

    The VariableAssignment class uses the ``total_ordering`` decorator so
    strict subsets, supersets and strict supersets are also available via the
    ``<``, ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.
    """

    def __init__(self, vocabulary, attribute_system, mapping, dummy=False):
        """
        Construct a VariableAssignment object.

        :param vocabulary: The Vocabulary object :math:`\Sigma` the \
        VariableAssignment is defined over.
        :type  vocabulary: Vocabulary
        :param attribute_system: The AttributeSystem object \
        :math:`\mathcal{S}` from which the objects \
        :math:`\{s_{1}, \ldots, s_{n}\}` in the VariableAssignment come from.
        :type  attribute_system: AttributeSystem
        :param mapping: The mapping :math:`\chi` from the variables V of \
        the Vocabulary object :math:`\Sigma` in the ``vocabulary`` parameter \
        to the objects :math:`\{s_{1}, \ldots, s_{n}\}` of the \
        AttributeSystem object :math:`\mathcal{A}` in the \
        ``attribute_system`` parameter.
        :type  mapping: ``dict``
        :param dummy: A flag for creating a dummy (i.e., empty) \
        VariableAssignment object :math:`\chi_{dummy}`.
        :type  dummy: ``bool``

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object, ``attribute_system`` parameter must be an AttributeSystem \
        object and ``mapping`` parameter must be a ``dict`` with ``str`` keys \
        and values.
        :raises ValueError: All keys in the ``mapping`` parameter must be in \
        the Vocabulary object in the ``vocabulary`` parameter's ``V`` member \
        and all values in the ``mapping`` parameter must be unique and match \
        some object in the ``object`` member of the AttributeSystem object in \
        the ``attribute_system`` parameter.
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
        Determine if two VariableAssignment objects are equal via the ``==``
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
        Retrive the object :math:`s_{i}` mapped to the variable :math:`v_{i}`
        given by ``key`` parameter via indexing
        (e.g. ``VariableAssignment[key]``).

        :param key: The variable :math:`v_{i}` to use for retrieval.
        :type  key: str

        :raises KeyError: The variable :math:`v_{i}` given by the ``key`` \
        parameter is not in this VariableAssignment's ``source`` member.
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
        Deepcopy a VariableAssignment object via the ``copy.deepcopy`` method.
        This does not break the reference to the underlying Vocabulary object
        :math:`\Sigma`.
        """

        from copy import deepcopy

        return VariableAssignment(
            self._vocabulary,
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def __str__(self):
        """
        Return a readable string representation of the VariableAssignment object.
        """

        return 'VA' + str(self._mapping)

    def __repr__(self):
        """Return a string representation of the VariableAssignment object."""
        return self.__str__()
