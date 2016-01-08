"""Attribute System class."""

from copy import deepcopy
from functools import total_ordering
from AttributeStructure import Attribute, Relation, AttributeStructure


@total_ordering
class AttributeSystem(object):
    """Class for Attribute System."""
    def __init__(self, A, objects):
        """Construct AttributeSystem object."""
        # Enforce objects as list of strings
        if not isinstance(objects, list):
            raise TypeError("objects parameter must be of type list")
        for obj in objects:
            if not isinstance(obj, str):
                raise ValueError(str(objects) + " must contain only strings")

            if obj == "":
                raise ValueError("Cannot add an empty string as object")

        # Enforce AttributeStructure type
        if not hasattr(A, "_is_AttributeStructure"):
            raise TypeError("A parameter must be of type AttributeStructure")

        # enforce no duplicate objects
        if len(objects) != len(set(objects)):
            raise ValueError(
                "dupicate objects not allowed in AttributeSystem")

        # sort objects before setting them
        self._objects = sorted(objects)
        self._attribute_structure = deepcopy(A)
        self._is_AttributeSystem = True

    def __eq__(self, other):
        """Implement == for AttributeSystem's."""
        c_astr = self._attribute_structure == other._attribute_structure
        c_objs = set(self._objects) == set(other._objects)
        if c_astr and c_objs:
            return True
        else:
            return False

    def __le__(self, other):
        """Implement <= operator for AttributeSystem; overloaded for subset."""
        c_astr = self._attribute_structure <= other._attribute_structure
        c_objs = set(self._objects) <= set(other._objects)
        if c_astr and c_objs:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != for AttributeSystem's."""
        return not self.__eq__(other)

    def __add__(self, other):
        """Implement + for AttributeSystem's."""
        self_copy = deepcopy(self)
        other_copy = deepcopy(other)

        # Handle adding an Attribute
        if hasattr(other_copy, "_is_Attribute"):
            self_copy._attribute_structure += other_copy
        # Handle adding a Relation
        elif hasattr(other_copy, "_is_Relation"):
            self_copy._attribute_structure += other_copy
        # Handle adding an AttributeStructure
        elif hasattr(other_copy, "_is_AttributeStructure"):
            self_copy._attribute_structure += other_copy
        # Handle adding an AttributeSystem
        elif hasattr(other_copy, "_is_AttributeSystem"):
            # try to add other_copy.AttributeStructure
            self_copy._attribute_structure += other_copy._attribute_structure
            # try to add objects; raise ValueError if there are duplicates
            if not set(self_copy._objects) & set(other_copy._objects):
                self_copy._objects = self_copy._objects + other_copy._objects
            else:
                raise ValueError(
                    "AttributeSystem cannot add duplicate objects from "
                    "other AttributeSystem")
        # Handle removing a list of objects or an object string
        else:
            raise TypeError(
                "Only strings, lists, Attributes, Relations, "
                "AttributeStructures, and AttributeSystems may be removed "
                "from an AttributeSystem")

        return self_copy

    def __sub__(self, other):
        """Implement - for AttributeSystem's."""
        self_copy = deepcopy(self)
        other_copy = deepcopy(other)

        # Handle removing an Attribute
        if hasattr(other_copy, "_is_Attribute"):
            self_copy._attribute_structure -= other_copy
        # Handle removing a Relation
        elif hasattr(other_copy, "_is_Relation"):
            self_copy._attribute_structure -= other_copy
        # Handle removing an AttributeStructure
        elif hasattr(other_copy, "_is_AttributeStructure"):
            self_copy._attribute_structure -= other_copy
        # Handle removing an AttributeSystem
        elif hasattr(other_copy, "_is_AttributeSystem"):
            # try to add other_copy.AttributeStructure
            self_copy._attribute_structure -= other_copy._attribute_structure
            # try to add objects; raise ValueError if there are duplicates
            if set(other_copy._objects) <= set(self_copy._objects):
                left_objs = set(self_copy._objects) - set(other_copy._objects)
                self_copy._objects = list(left_objs)
            else:
                raise ValueError(
                    "AttributeSystem cannot remove objects present in "
                    "other AttributeSystem if they do not exist in this "
                    "AttributeSystem")
        # Handle removing a list of objects or an object string
        else:
            raise TypeError(
                "Only strings, lists, Attributes, Relations, "
                "AttributeStructures, and AttributeSystems may be removed "
                "from an AttributeSystem")

        return self_copy

    def __iadd__(self, other):
        """Implement += operator for AttributeSystem."""
        return self.__add__(other)

    def __isub__(self, other):
        """Implement -= for AttributeSystem."""
        return self.__sub__(other)

    def __getitem__(self, obj):
        """Implement indexing for AttributeSystem."""
        # Handle removing an Attribute
        if hasattr(obj, "_is_Attribute"):
            return self._attribute_structure[obj]
        # Handle removing a Relation
        elif hasattr(obj, "_is_Relation"):
            return self._attribute_structure[obj]
        # Handle removing a list of objects or an object string
        else:
            if isinstance(obj, str):
                if obj in self._objects:
                    return self._objects[self._objects.index(obj)]
            else:
                raise TypeError(
                    "Only strings (refering to objects), Attributes, and "
                    "Relations may index an AttributeSystem")

    def __contains__(self, key):
        """Implement in for AttributeSystem."""
        # Handle removing an Attribute
        if hasattr(key, "_is_Attribute"):
            return key in self._attribute_structure
        # Handle removing a Relation
        elif hasattr(key, "_is_Relation"):
            return key in self._attribute_structure
        elif hasattr(key, "_is_AttributeStructure"):
            return key == self._attribute_structure
        # Handle removing a list of objects or an object string
        else:
            if isinstance(key, str):
                if key in self._objects:
                    return True
            else:
                raise TypeError(
                    "Only strings, Attributes, and Relations may be checked "
                    "for membership in an AttributeSystem")

    def __deepcopy__(self, memo):
        """Return a deep copy of this AttributeSystem object."""
        objects_copy = deepcopy(self._objects)
        attribute_structure_copy = deepcopy(self._attribute_structure)
        return AttributeSystem(attribute_structure_copy, objects_copy)

    def get_power(self):
        """Get power of this AttributeSystem, i.e., n * |A|."""
        return len(self._objects) * self._attribute_structure.get_cardinality()

    def __str__(self):
        """Return human-readable string representation of AttributeSystem."""
        asys_str = '({' + ''.join([s_i + ', ' for s_i in self._objects])[:-2]
        asys_str += '} ; ' + str(self._attribute_structure) + ')'
        return asys_str

    def __repr__(self):
        """Machine representation of this AttributeSystem; same as str()."""
        return self.__str__()

    def is_automorphic(self):
        """Determine if Attribute System is automorphic."""
        from ValueSet import ValueSet
        # Check if any object is a subset of value set of any attribute
        for s in self._objects:
            for a in self._attribute_structure._attributes:
                if ValueSet([s]) <= a._value_set:
                    return True
        return False


def main():
    """Main method for quick tests."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"], 1)

    a = AttributeStructure(a, b, c, r)
    o = ['o3', 'o1', 'o5', 'o2', 'o4']

    asys = AttributeSystem(a, o)
    print asys <= asys
    print asys < asys

if __name__ == "__main__":
    main()
