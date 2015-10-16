"""
This module provides constant and variable assignment objects which
remember the vocabulary and objects used during the mapping process
through and OOP perspective.
"""

from Vocabulary import Vocabulary
from Base import Attribute, AttributeStructure, AttributeSystem

class Assignment(object):
    """This is a superclass for generic assignments."""

    def __init__(self, vocabulary, attribute_system):
        """
        Initialize a base Assignment with a mapping from some
        vocabulary to a set of objects while keeping a copy of the
        vocabulary an dobjects themselves.

        Raise TypeError if vocabulary parameter is not of type
        Vocabulary, attribute_system parameter are not of type list,
        or mapping parameter is not of type dict.
        """

        if not isinstance(vocabulary, Vocabulary):
            raise TypeError(
                "vocabulary parameter must be of type Vocabulary")

        if not isinstance(attribute_system, AttributeSystem):
            raise TypeError(
                "objects parameter must be of type list")

        self._vocabulary = vocabulary
        self._attribute_system = attribute_system
        self._objects = attribute_system.get_objects()

    def __eq__(self, other):
        """Determine if self == other."""
        vocabulary_condition = self.get_vocabulary() == other.get_vocabulary()
        objects_condition = self.get_objects() == other.get_objects()

        if vocabulary_condition and objects_condition:
            return True
        else:
            return False

    def __ne__(self, other):
        """Determine if self != other."""
        vocabulary_condition = self.get_vocabulary() == other.get_vocabulary()
        objects_condition = self.get_objects() == other.get_objects()

        if not vocabulary_condition or not objects_condition:
            return True
        else:
            return False

    def get_vocabulary(self):
        """Return this Assignment's Vocabulary object."""
        return self._vocabulary

    def get_attribute_system(self):
        """Return this Assignment's AttributeSystem object."""
        return self._attribute_system

    def get_objects(self):
        """Return this Assignment's objects list."""
        return self._objects


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

        Raise TypeError if mapping parameter is not of type dict.
        Raise ValueError if mapping source (i.e., its keys) is not a
        subset of Vocabulary's constants or if mapping target (i.e.,
        its values) are not a subset of AttributeSystem's object list.
        Raise ValueError if mapping values contains duplicate items.
        """

        if not isinstance(mapping, dict):
            raise TypeError(
                "mapping parameter must be of type dict")

        Assignment.__init__(self, vocabulary, attribute_system)

        source = mapping.keys()
        target = mapping.values()

        if len(target) != len(set(target)):
            raise ValueError(
                "duplicate values in mapping parameter "
                "are not allowed; mapping must be 1-to-1.")

        #note: Vocabularies prevent duplicates as do dictionary keys
        source_condition = set.issubset(set(source), set(vocabulary.get_C()))
        #note: AttributeSystems prevent duplicate objects
        target_condition = set.issubset(set(target), set(self.get_objects()))

        if source_condition and target_condition:
            self._mapping = mapping
        else:
            raise ValueError(
                "ConstantAssignment must be a partial (or total) function "
                "from vocabulary.get_C() to attribute_system.get_objects()")

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
        """Return the source of this ConstantAssignment's mapping."""
        return self.get_mapping().keys()

    def get_target(self):
        """Return the target of this ConstantAssignment's mapping."""
        return self.get_mapping().values()

    def is_total(self):
        """
        Determine if this ConstantAssignment is a total function
        from C to {s_1,...,s_n}.
        """

        C = self.get_vocabulary().get_C()
        source = self.get_source()

        #note: we already know from constructor that objs is a subset of C
        #we just need to check that lengths are equal
        if len(C) == len(source):
            return True
        else:
            return False

    def get_domain(self):
        """
        Get the set of all and only those constant symbols for which p
        is defined w.r.t. ConstantAssignment's Vocabulary object.
        """
        
        source = self.get_source()
        C = self.get_vocabulary().get_C()

        return [key for key in source if key in C]

    def __str__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'C' + str(self.get_mapping())

    def __repr__(self):
        """Return a string of this ConstantAssignment's mapping."""
        return 'C' + str(self.get_mapping())


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

        Raise TypeError if mapping parameter is not of type dict.
        Raise ValueError if mapping source (i.e., its keys) is not equal
        to Vocabulary's set of variables or if mapping target (i.e.,
        its values) are not a subset of AttributeSystem's object list.
        Raise ValueError if mapping values contains duplicate items.
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

def main():
    """
    main method called when Assignment.py is executed;
    used for testing.
    """

    attribute = Attribute('hour', ['0,...,23'])
    astr = AttributeStructure(attribute)

    sigma = Vocabulary(['C1', 'C2'], [], ['V1', 'V2'])

    objs = ['c1', 'c2', 'x1', 'x2']
    asys = AttributeSystem(objs, astr)

    const_mapping = {'C1': 'c1', 'C2': 'c2'}
    var_mapping = {'V1': 'x1', 'V2': 'x2'}
    p = ConstantAssignment(sigma, asys, const_mapping)
    X = VariableAssignment(sigma, asys, var_mapping)

    print p.is_total()
    print X.get_source()
    print X.get_target()

if __name__ == "__main__":
    main()
