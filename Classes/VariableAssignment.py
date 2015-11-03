"""Variable Assignment class."""

from vivid.Classes.Assignment import Assignment

class VariableAssignment(Assignment):
    """
    Class to represent a Variable Assignment or a total mapping from the
    variable symbols in a Vocabulary to the objects in an AttributeSystem.
    """

    def __init__(self, vocabulary, attribute_system, mapping, dummy=False):
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

        if dummy:
            self._mapping = {}
        else:
            source = mapping.keys()
            target = mapping.values()

            if len(source) != len(set(source)) or len(target) != len(set(target)):
                raise ValueError(
                    "duplicate values in mapping parameter "
                    "are not allowed; mapping must be 1-to-1.")

            #total mapping so check for equality
            source_condition = set(source) == set(vocabulary._V)

            target_condition = set(target) <= set(attribute_system._objects)

            if source_condition and target_condition:
                Assignment.__init__(self, vocabulary, attribute_system)
                self._mapping = mapping
                self._source = mapping.keys()
                self._target = mapping.values()
                self._is_ConstantAssignment = True
            else:
                raise ValueError(
                    "VariableAssignment must be a total function from "
                    "vocabulary._V to attribute_system._objects")

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
        """Implement != operator ConstantAssignment objects."""
        return not self.__eq__(other)

    def __getitem__(self, key):
        """Implement indexing for VariableAssignment object."""
        if not isinstance(key, str):
            raise TypeError("key parameter must be of type string")

        try:
            return self._mapping[key]
        except KeyError:
            raise KeyError(str(key) + " is not in source")

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for VariableAssignment object."""
        from copy import deepcopy
        
        return VariableAssignment(
            deepcopy(self._vocabulary),
            deepcopy(self._attribute_system),
            deepcopy(self._mapping))

    def __str__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'VA' + str(self._mapping)

    def __repr__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return self.__str__()
