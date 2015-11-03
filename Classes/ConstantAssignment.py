"""Constant Assignemnt object."""

from vivid.Classes.Assignment import Assignment

class ConstantAssignment(Assignment):
    """
    Class to represent a constant assignment from Assignment's
    Vocabulary object's constants to the set of objects contained
    in Assignment's AttributeSystem's list of objects.
    """

    def __init__(self, vocabulary, attribute_system, mapping):
        """
        Initialize a ConstantAssignment object with a mapping from the
        Vocabulary's constants to the AttributeSystem's list of objects.
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

        if len(source) != len(set(source)) or len(target) != len(set(target)):
            raise ValueError(
                "duplicate values in mapping parameter "
                "are not allowed; mapping must be 1-to-1.")
        
        #note: Vocabularies prevent duplicates as do dictionary keys
        source_condition = set(source) <= set(vocabulary._C)
        #note: AttributeSystems prevent duplicate objects
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
        Determine if self == other for
        self and other ConstantAssignment objects.
        """

        vocabulary_cond = self._vocabulary == other._vocabulary
        asys_cond = self._attribute_system == other._attribute_system
        mapping_cond = self._mapping == other._mapping

        if vocabulary_cond and asys_cond and mapping_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement == operator ConstantAssignment objects."""
        return not self.__eq__()

    def __deepcopy__(self):
        """Return a deep copy of this ConstantAssignment object."""
        from copy import deepcopy
        
        return ConstantAssignment(
            deepcopy(self._vocabulary),
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def is_total(self):
        """
        Determine if this ConstantAssignment is a total function
        from C to {s_1,...,s_n}.
        """
        source_len = len(self._source)
        target_len = len(self._target)
        C_len = len(self._C)
        attribute_system_len = len(self._asys)

        if source_len == target_len == C_len == attribute_system_len:
            return True
        else:
            return False

    def get_domain(self):
        """
        Get the set of all and only those constant symbols for which p
        is defined w.r.t. ConstantAssignment's Vocabulary object.
        """

        return [key for key in self._source if key in self._vocabulary._C]

    @staticmethod
    def in_conflict(p1, p2):
        """Check if p1 is in conflict with p2."""
        union_domain = set(p1.get_domain()) & set(p2.get_domain())

        for c in union_domain:
            if p1._mapping[c] != p2._mapping[c]:
                return True

        return False

    def __str__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'C' + str(self._mapping)

    def __repr__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return self.__str__()
