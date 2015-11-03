"""Variable Assignment class."""

from vivid.Classes.Assignment import Assignment

class VariableAssignment(Assignment):
    """
    Class to represent a variable assignment from Assignment's
    Vocabulary object's variables to the set of objects contained
    in Assignment's AttributeSystem's list of objects.
    """

    def __init__(self, vocabulary, attribute_system, mapping, dummy=False):
        """
        Initialize a ConstantAssignment object with a mapping from the
        Vocabulary's constants to the AttributeSystem's list of objects.
        """

        if not isinstance(mapping, dict):
            raise TypeError(
                "mapping parameter must be of type dict")

        Assignment.__init__(self, vocabulary, attribute_system)

        if dummy:
            self._mapping = {}
        else:
            source = mapping.keys()
            target = mapping.values()

            if len(target) != len(set(target)):
                raise ValueError(
                    "duplicate values in mapping parameter "
                    "are not allowed; mapping must be 1-to-1.")

            #note: Vocabularies prevent duplicates as do dictionary keys
            #but converting to sets allows unordered equality comparison.
            source_condition = set(source) == set(vocabulary.get_V())
            #source_condition = set.issubset(set(source), set(vocabulary.get_V()))
            #note: AttributeSystems prevent duplicate objects
            target_condition = set.issubset(
                set(target), set(self.get_objects()))

            if source_condition and target_condition:
                self._mapping = mapping
            else:
                raise ValueError(
                    "VariableAssignment must be a total function from "
                    "vocabulary.get_V() to attribute_system.get_objects()")

    def __eq__(self, other):
        """
        Determine if self == other for
        self and other ConstantAssignment objects.
        """

        vocabulary_cond = self.get_vocabulary() == other.get_vocabulary()
        attribute_system_cond = \
            self.get_attribute_system() == other.get_attribute_system()
        mapping_cond = self.get_mapping() == other.get_mapping()

        if vocabulary_cond and attribute_system_cond and mapping_cond:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if self != other for
        self and other ConstantAssignment objects.
        """

        vocabulary_cond = self.get_vocabulary() == other.get_vocabulary()
        attribute_system_cond = \
            self.get_attribute_system() == other.get_attribute_system()
        mapping_cond = self.get_mapping() == other.get_mapping()

        if vocabulary_cond and attribute_system_cond and mapping_cond:
            return False
        else:
            return True

    def deep_copy(self):
        """Return a deep copy of this ConstantAssignment object."""
        import copy

        vocabulary_copy = self._vocabulary.deep_copy()
        attribute_system_copy = self._attribute_system.deep_copy()
        mapping_copy = copy.copy(self._mapping)

        return ConstantAssignment(
            vocabulary_copy, attribute_system_copy, mapping_copy)

    def get_mapping(self):
        """Return this ConstantAssignment's mapping."""
        return self._mapping

    def get_source(self):
        """Return the source of this VariableAssignment's mapping."""
        return self.get_mapping().keys()

    def get_target(self):
        """Return the target of this VariableAssignment's mapping."""
        return self.get_mapping().values()

    def __str__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'V' + str(self.get_mapping())

    def __repr__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'V' + str(self.get_mapping())