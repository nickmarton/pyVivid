"""This section introduces the ConstantAssignment class."""

from functools import total_ordering
from assignment import Assignment


@total_ordering
class ConstantAssignment(Assignment):
    """
    ConstantAssignment class. A ConstantAssignment is a partial
    function :math:`\\rho` from the constants C of some Vocabulary object
    :math:`\Sigma`, to the objects :math:`\{s_{1}, \ldots, s_{n}\}` of some
    AttributeSystem :math:`\mathcal{S}`.

    The ConstantAssignment class uses the ``total_ordering`` decorator so
    strict subsets, supersets and strict supersets are also available via the
    ``<``, ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.

    :ivar vocabulary: A reference to the Vocabulary object :math:`\Sigma` the \
    ConstantAssignment is defined over.
    :ivar attribute_system: A copy of the AttributeSystem object \
    :math:`\mathcal{S}` the ConstantAssignment originates from.
    :ivar mapping: The mapping C :math:`\longmapsto \{s_{1}, \ldots, s_{n}\}`.
    :ivar source: The constants of :math:`\Sigma` used in the partial \
    mapping :math:`\\rho`.
    :ivar target: The objects of :math:`\mathcal{S}` used in the partial \
    mapping :math:`\\rho`.
    :ivar _is_ConstantAssignment: An identifier to use in place of ``type`` \
    or ``isinstance``.
    """

    def __init__(self, vocabulary, attribute_system, mapping):
        """
        Construct a ConstantAssignment object.

        :param vocabulary: The Vocabulary object :math:`\Sigma` the \
        ConstantAssignment is defined over.
        :type  vocabulary: Vocabulary
        :param attribute_system: The AttributeSystem object \
        :math:`\mathcal{S}` from which the objects \
        :math:`\{s_{1}, \ldots, s_{n}\}` in the ConstantAssignment come from.
        :type  attribute_system: AttributeSystem
        :param mapping: The mapping :math:`\\rho` from the constants C of \
        the Vocabulary object :math:`\Sigma` in the ``vocabulary`` parameter \
        to the objects :math:`\{s_{1}, \ldots, s_{n}\}` of the \
        AttributeSystem object :math:`\mathcal{A}` in the \
        ``attribute_system`` parameter.
        :type  mapping: ``dict``

        :raises TypeError: ``vocabulary`` parameter must be a Vocabulary \
        object, ``attribute_system`` parameter must be an AttributeSystem \
        object and ``mapping`` parameter must be a ``dict`` with ``str`` keys \
        and values.
        :raises ValueError: All keys in the ``mapping`` parameter must be in \
        the Vocabulary object in the ``vocabulary`` parameter's ``C`` member \
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
        Overloaded ``<`` operator for ConstantAssignment. Determine if the
        calling ConstantAssignment object is a subset of the ConstantAssignment
        object in the ``other`` parameter.

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
        Retrive the object :math:`s_{i}` mapped to the constant :math:`c_{i}`
        given by ``key`` parameter via indexing
        (e.g. ``ConstantAssignment[key]``).

        :param key: The constant :math:`c_{i}` to use for retrieval.
        :type  key: str

        :raises KeyError: The constant :math:`c_{i}` given by the ``key`` \
        parameter is not in this ConstantAssignment's ``source`` member.
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
        This does not break the reference to the underlying Vocabulary object
        :math:`\Sigma`.
        """

        from copy import deepcopy

        return ConstantAssignment(
            self._vocabulary,
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def add_mapping(self, constant_symbol, obj):
        """
        Extend the calling ConstantAssignment object by adding a new mapping
        from the constant :math:`c^{\prime}` in the ``constant_symbol``
        parameter to the object :math:`o^{\prime}` in the ``obj`` parameter.

        :raises TypeError: Both ``constant_symbol`` and ``obj`` parameters \
        must be ``str``\s.
        :raises ValueError: The constant :math:`c^{\prime}` in the \
        ``constant_symbol`` parameter must be in the ``C`` member of the \
        underlying Vocabulary object :math:`\Sigma`, the object \
        :math:`o^{\prime}` in the ``obj`` parameter must be in the objects of \
        the ``objects`` member of the underlying AttributeSystem object \
        :math:`\mathcal{S}` and neither the constant :math:`c^{\prime}` nor \
        the object :math:`o^{\prime}` may be a duplicate.
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
        Extend the calling ConstantAssignment object by removing an existing
        mapping from the constant :math:`c^{\prime}` in the ``constant_symbol``
        parameter to the object :math:`o^{\prime}` in the ``obj`` parameter.

        :raises TypeError: both ``constant_symbol`` and ``obj`` parameters \
        must be ``str``\s.
        :raises ValueError: The constant :math:`c^{\prime}` in the \
        ``constant_symbol`` parameter must be in the ``C`` member of the \
        underlying Vocabulary object :math:`\Sigma`, the object \
        :math:`o^{\prime}` in the ``obj`` parameter must be in the objects of \
        the ``objects`` member of the underlying AttributeSystem object \
        :math:`\mathcal{S}` and the constant :math:`c^{\prime}` and \
        the object :math:`o^{\prime}` must already be in the ``source`` and \
        ``target`` members of the calling ConstantAssignment object \
        respectively.
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
        Determine if the calling ConstantAssignment object :math:`\\rho` is a \
        total function :math:`\widehat{\\rho}` from C \
        :math:`\\longrightarrow \{s_{1}, \ldots, s_{n}\}`.

        :return: Whether or not the source of :math:`\\rho` spans the ``C`` \
        member of :math:`\Sigma`.
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
        Get the set of all and only those constant symbols for which the
        calling ConstantAssignment object :math:`\\rho` is defined w.r.t. the
        ``C`` member of the ``vocabulary`` member of :math:`\\rho`.

        :return: The list of constants for which :math:`\\rho` is defined.
        :rtype: ``list``
        """

        return list(self._source)

    def in_conflict(self, other):
        """
        Check if the calling ConstantAssignment object :math:`\\rho_{1}` is in
        conflict with the ConstantAssignment object :math:`\\rho_{2}` provided
        in the ``other`` parameter.

        :return: Whether or not :math:`\\rho_{1}` and :math:`\\rho_{2}` are \
        in conflict, that is, if there is some \
        :math:`{c \in Dom(\\rho_{1}) \cap Dom(\\rho_{2})}`, such that \
        :math:`\\rho_{1}(c) \\ne \\rho_{2}(c)`.
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
        Return a readable string representation of the ConstantAssignment
        object.
        """

        return 'CA' + str(self._mapping)

    def __repr__(self):
        """Return a string representation of the ConstantAssignment object."""
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
