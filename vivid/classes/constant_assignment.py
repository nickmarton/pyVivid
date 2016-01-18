"""constant_assignemnt module."""

from functools import total_ordering
from assignment import Assignment


@total_ordering
class ConstantAssignment(Assignment):
    """
    ConstantAssignment class. A ConstantAssignment is a partial
    function :math:`\\rho` from the constants C of some Vocabulary to the
    objects {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`} of some AttributeSystem.

    The ConstantAssignment class uses the ``total_ordering`` decorator so
    strict subsets, supersets and strict supersets are also available via the
    ``<``, ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.

    :ivar vocabulary: a reference to the Vocabulary object the \
    ConstantAssignment is defined over.
    :ivar attribute_system: a copy of the AttributeSystem the \
    ConstantAssignment originates from.
    :ivar mapping: The mapping C :math:`\longmapsto` \
    {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`}
    :ivar source: The constants used in the partial mapping :math:`\\rho`.
    :ivar target: The objects used in the partial mapping :math:`\\rho`.
    :ivar _is_ConstantAssignment: An identifier to use in place of type or \
    isinstance.
    """

    def __init__(self, vocabulary, attribute_system, mapping):
        """
        Construct a ConstantAssignment object.

        :param vocabulary: The Vocabulary the ConstantAssignment is defined over.
        :type  vocabulary: Vocabulary
        :param attribute_system: The AttributeSystem from which the objects \
        in the Assignment come from.
        :type  attribute_system: AttributeSystem
        :param mapping: The mapping :math:`\\rho` from the constants C of \
        ``vocabulary`` to the objects \
        {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`} of ``attribute_system``.
        :type  mapping: ``dict``

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object, ``attribute_system`` parameter must be an AttributeSystem \
        object and ``mapping`` parameter must be a ``dict`` with ``str`` keys \
        and values.
        :raises ValueError: all keys in ``mapping`` parameter must be in \
        ``vocabulary`` parameter's constants and all values in ``mapping`` \
        parameter must be unique and match some object in \
        ``attribute_system`` parameter.
        """

        if not isinstance(mapping, dict):
            raise TypeError(
                "mapping parameter must be of type dict")

        if not all([isinstance(s, str) for s in mapping.keys()]):
            raise TypeError("mapping must be of form str: str")

        if not all([isinstance(s, str) for s in mapping.values()]):
            raise TypeError("mapping must be of form str: str")

        source = mapping.keys()
        target = mapping.values()

        if len(target) != len(set(target)):
            raise ValueError(
                "duplicate values in mapping parameter "
                "are not allowed; mapping must be 1-to-1.")

        # note: Vocabularies prevent duplicates as do dictionary keys
        source_condition = set(source) <= set(vocabulary._C)
        # note: AttributeSystems prevent duplicate objects
        target_condition = set(target) <= set(attribute_system._objects)

        if source_condition and target_condition:
            Assignment.__init__(self, vocabulary, attribute_system)
            self._mapping = mapping
            self._source = mapping.keys()
            self._target = mapping.values()
            self._is_ConstantAssignment = True
        else:
            raise ValueError(
                "ConstantAssignment must be a partial (or total) function "
                "from Vocabulary's C to AttributeSystem's objects")

    def __eq__(self, other):
        """
        Determine if two ConstantAssignment objects are equal via the ``==``
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
        Determine if two ConstantAssignment objects are not equal via the
        ``!=`` operator.
        """

        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Overloaded ``<`` operator for ConstantAssignment. Determine if this
        ConstantAssignment is a subset of the ConstantAssignment contained in
        ``other`` parameter.

        :raises TypeError: ``other`` parameter must be a ConstantAssignment \
        object.
        """

        if not hasattr(other, "_is_ConstantAssignment"):
            raise TypeError("other must be of type ConstantAssignment")

        same_attr_systems = self._attribute_system == other._attribute_system
        same_vocabularies = self._vocabulary == other._vocabulary

        if not same_attr_systems or not same_vocabularies:
            return False

        return set(self._mapping.items()) < set(other._mapping.items())

    def __getitem__(self, key):
        """
        Retrive the object mapped to the constant given by ``key`` parameter
        via indexing (e.g. ``ConstantAssignment[key]``).

        :param key: The constant to use for retrieval.
        :type  key: str

        :raises KeyError: constant given by ``key`` parameter is not in this \
        ConstantAssignment's ``source``.
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

        return ConstantAssignment(
            self._vocabulary,
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def add_mapping(self, constant_symbol, obj):
        """
        Extend this ConstantAssignment by adding new mapping from
        constant in ``constant_symbol`` parameter to object in ``obj``
        parameter.

        :raises TypeError: both ``constant_symbol`` and ``obj`` parameters \
        must be ``str``\s.
        :raises ValueError: constant in ``constant_symbol`` parameter must be \
        in ``vocabulary`` member, object in ``obj`` parameter must be in the \
        objects of ``attribute_system`` member and neither the constant nor \
        the object may be a duplicate.
        """

        if type(constant_symbol) is not str or type(obj) is not str:
            raise TypeError(
                "constant_symbol and obj parameters must be strings")

        if constant_symbol not in self._vocabulary._C:
            raise ValueError(
                "constant_symbol parameter must be in vocabulary.")
        if obj not in self._attribute_system._objects:
            raise ValueError(
                "obj parameter must be contained in objects of "
                "AttributeSystem")
        if constant_symbol in self._source:
            raise ValueError("constant_symbol already in ConstantAssignment")
        if obj in self._target:
            raise ValueError("obj already in ConstantAssignment")

        self._mapping[constant_symbol] = obj
        self._source.append(constant_symbol)
        self._target.append(obj)

    def remove_mapping(self, constant_symbol, obj):
        """
        Extend this ConstantAssignment by removing new mapping from
        constant in ``constant_symbol`` parameter to object in ``obj``
        parameter.

        :raises TypeError: both ``constant_symbol`` and ``obj`` parameters \
        must be ``str``\s.
        :raises ValueError: constant in ``constant_symbol`` parameter must be \
        in ``vocabulary`` member, object in ``obj`` parameter must be in the \
        objects of ``attribute_system`` member and the constant and object \
        must be in the source and target of the mapping respectively.
        """

        if type(constant_symbol) is not str or type(obj) is not str:
            raise TypeError(
                "constant_symbol and obj parameters must be strings")

        if constant_symbol not in self._vocabulary._C:
            raise ValueError(
                "constant_symbol parameter must be in vocabulary.")
        if obj not in self._attribute_system._objects:
            raise ValueError(
                "obj parameter must be contained in objects of "
                "AttributeSystem")
        if constant_symbol not in self._source:
            raise ValueError("constant_symbol not in ConstantAssignment")
        if obj not in self._target:
            raise ValueError("obj not in ConstantAssignment")

        if self._mapping[constant_symbol] != obj:
            raise ValueError("Invalid mapping provided")

        del self._mapping[constant_symbol]
        self._source.remove(constant_symbol)
        self._target.remove(obj)

    def is_total(self):
        """
        Determine if this ConstantAssignment is a total function \
        :math:`\widehat{\\rho}` from C :math:`\\longrightarrow` \
        {s\ :sub:`1`, :math:`\ldots`, s\ :sub:`n`}.

        :return: whether ot not the source of this ConstantAssignment's \
        mapping covers all of its ``vocabulary`` member's C.
        :rtype: ``bool``
        """

        source_len = len(self._source)
        C_len = len(self._vocabulary._C)

        if source_len == C_len:
            return True
        else:
            return False

    def get_domain(self):
        """
        Get the set of all and only those constant symbols for which
        :math:`\\rho` is defined w.r.t. ConstantAssignment's ``vocabulary``
        member.

        :return: list of constants for which :math:`\\rho` is defined.
        :rtype: ``list``
        """

        return list(self._source)

    def in_conflict(self, other):
        """
        Check if this ConstantAssignment is in conflict with ConstantAssignment
        in ``other`` parameter.

        :return: whether or not this ConstantAssignment and the \
        ConstantAssignment in ``other`` are in conflict.
        :rtype: ``bool``

        :raises TypeError: ``other`` parameter must be a ConstantAssignment \
        object.
        """

        if not hasattr(other, "_is_ConstantAssignment"):
            raise TypeError(
                "other parameter must be a ConstantAssignment object")

        union_domain = set(self.get_domain()) & set(other.get_domain())

        for c in union_domain:
            if self._mapping[c] != other._mapping[c]:
                return True

        return False

    def __str__(self):
        """
        Return a readable string representation of a ConstantAssignment object.
        """

        return 'CA' + str(self._mapping)

    def __repr__(self):
        """Return a string representation of a ConstantAssignment object."""
        return self.__str__()


def main():
    """."""
    from vocabulary import Vocabulary
    from attribute import Attribute
    from attribute_structure import AttributeStructure
    from attribute_system import AttributeSystem

    vocabulary = Vocabulary(['C'], [], ['V'])

    a = Attribute("a", [])
    b = Attribute("b", [])
    astr = AttributeStructure(a, b)
    objs = ['a', 'b', 'c']
    attribute_system = AttributeSystem(astr, objs)

    C = ConstantAssignment(vocabulary, attribute_system, {'C': 'a'})
    print C._vocabulary
    vocabulary.add_constant("C2")
    print C._vocabulary

if __name__ == "__main__":
    main()
