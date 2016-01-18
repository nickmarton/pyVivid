"""attribute_system module."""

from copy import deepcopy
from functools import total_ordering
from attribute import Attribute
from relation import Relation
from attribute_structure import AttributeStructure


@total_ordering
class AttributeSystem(object):
    """
    AttributeSystem class composed of an AttributeStructure and set of objects,
    i.e.,

    .. centered:: :math:`\mathcal{S} =` \
    ({*s*\ :sub:`1`, :math:`\ldots`, *s*\ :sub:`n`}; :math:`\mathcal{A}`)

    The AttributeSystem class uses the ``total_ordering`` decorator so
    strict subsets, supersets and strict supersets are also available via the
    ``<``, ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.

    :ivar attribute_structure: The AttributeStructure of the AttributeSystem.
    :ivar objects: The objects of the AttributeSystem; held as a list of \
    ``str``\s.
    :ivar _is_AttributeSystem: An identifier to use in place of type or \
    isinstance.
    """

    def __init__(self, A, objects):
        """
        Construct AttributeSystem object.

        :param A: an AttributeStructure object to use as the attribute \
        structure of the AttributeSystem object.
        :type  A: AttributeStructure
        :param objects: A list of ``str``\s denoting the objects of the \
        AttributeSystem.
        :type  objects: list

        :raises TypeError: ``objects`` parameter must be a ``list`` and ``A`` \
        parameter must be an AttributeStructure object.
        :raises ValueError: all objects provided in ``objects`` parameter \
        must be unique non-empty ``str``\s.
        """

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
        """
        Determine if two AttributeSystem objects are equal via ``==`` operator.
        """

        c_astr = self._attribute_structure == other._attribute_structure
        c_objs = set(self._objects) == set(other._objects)
        if c_astr and c_objs:
            return True
        else:
            return False

    def __le__(self, other):
        """
        Determine if this AttributeSystem is a subset of the AttributeSystem
        contained in ``other`` parameter via ``<=`` operator.
        """

        c_astr = self._attribute_structure <= other._attribute_structure
        c_objs = set(self._objects) <= set(other._objects)
        if c_astr and c_objs:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two AttributeSystem objects are not equal via ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Add an Attribute, Relation, AttributeStructure, or AttributeSystem
        object via the ``+`` operator.

        :param other: The object to combine with the AttributeSystem. \
        An AttributeSystem is always returned regardless of the type of \
        ``other`` parameter.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        Relation, AttributeStructure, or AttributeSystem object.
        :raises ValueError: Cannot add AttributeSystems with overlapping \
        objects.
        """

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
        else:
            raise TypeError(
                "Only Attributes, Relations, AttributeStructures, and "
                "AttributeSystems may be removed from an AttributeSystem")

        return self_copy

    def __sub__(self, other):
        """
        Remove an Attribute, Relation, AttributeStructure, or AttributeSystem
        object via the ``-`` operator. In the case of AttributeStructure and
        AttributeSystem objects, remove all of their consituent parts from this
        AttributeSystem.

        :param other: The object to remove from the AttributeSystem. \
        An AttributeSystem is always returned regardless of the type of \
        ``other`` parameter.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        Relation, AttributeStructure, or AttributeSystem object.
        :raises ValueError: Cannot remove objects not present in this \
        AttributeSystem.
        """

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
        else:
            raise TypeError(
                "Only Attributes, Relations, AttributeStructures, and "
                "AttributeSystems may be removed from an AttributeSystem")

        return self_copy

    def __iadd__(self, other):
        """
        Add an Attribute, Relation, AttributeStructure, or AttributeSystem
        object via the ``+=`` operator.

        :param other: The object to combine with the AttributeSystem. \
        An AttributeSystem is always returned regardless of the type of \
        ``other`` parameter.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        Relation, AttributeStructure, or AttributeSystem object.
        :raises ValueError: Cannot add AttributeSystems with overlapping \
        objects.
        """

        return self.__add__(other)

    def __isub__(self, other):
        """
        Remove an Attribute, Relation, AttributeStructure, or AttributeSystem
        object via the ``-=`` operator. In the case of AttributeStructure and
        AttributeSystem objects, remove all of their consituent parts from this
        AttributeSystem.

        :param other: The object to remove from the AttributeSystem. \
        An AttributeSystem is always returned regardless of the type of \
        ``other`` parameter.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        Relation, AttributeStructure, or AttributeSystem object.
        :raises ValueError: Cannot remove objects not present in this \
        AttributeSystem.
        """

        return self.__sub__(other)

    def __getitem__(self, key):
        """
        Retrieve a reference to the Attribute, Relation, or object in the
        AttributeSystem via the key provided.

        :param key: The Attribute, Relation or name of the object to get the \
        reference of from this AttributeSystem.
        :type  key: Attribute|Relation|str

        :raises TypeError: ``str`` in ``key`` does not match any object \
        contained in this AttributeSystem.
        """

        # Handle removing an Attribute
        if hasattr(key, "_is_Attribute"):
            return self._attribute_structure[key]
        # Handle removing a Relation
        elif hasattr(key, "_is_Relation"):
            return self._attribute_structure[key]
        # Handle removing a list of objects or an object string
        else:
            if isinstance(key, str):
                if key in self._objects:
                    return self._objects[self._objects.index(key)]
            else:
                raise TypeError(
                    "Only strings (refering to objects), Attributes, and "
                    "Relations may index an AttributeSystem")

    def __contains__(self, key):
        """
        Determine if Attribute, Relation, AttributeStructure, or ``str`` in \
        ``key`` parameter is contained by this AttributeSystem via ``in`` \
        operator.

        :param key: The key to use when checking for membership.
        :type  key: Attribute|Relation|AttributeStructure|str

        :raises TypeError: ``key`` must be an Attribute object, \
        Relation object, AttributeStructure object, or ``str``.
        """

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
        """
        Deepcopy an AttributeSystem object via the ``copy.deepcopy`` method.
        """

        objects_copy = deepcopy(self._objects)
        attribute_structure_copy = deepcopy(self._attribute_structure)
        return AttributeSystem(attribute_structure_copy, objects_copy)

    def get_power(self):
        """
        Get power of this AttributeSystem, i.e.,
        *n* :math:`\cdot` :math:`\lvert`\ :math:`\mathcal{A}`\ :math:`\lvert`.

        :return: power of the AttributeSystem: \
        *n* :math:`\cdot` :math:`\lvert`\ :math:`\mathcal{A}`\ :math:`\lvert`
        :rtype: ``int``
        """

        return len(self._objects) * self._attribute_structure.get_cardinality()

    def __str__(self):
        """
        Return a readable string representation of the AttributeSystem object.
        """

        asys_str = '({' + ''.join([s_i + ', ' for s_i in self._objects])[:-2]
        asys_str += '} ; ' + str(self._attribute_structure) + ')'
        return asys_str

    def __repr__(self):
        """
        Return a string representation of the AttributeSystem object.
        """

        return self.__str__()

    def is_automorphic(self):
        """
        Determine if this Attribute System is automorphic.

        :return: Whether or not this AttributeSystem is automorphic; i.e., \
        some object is contained by one of the ValueSets of the Attributes.
        :rtype: ``bool``
        """

        from valueset import ValueSet
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
