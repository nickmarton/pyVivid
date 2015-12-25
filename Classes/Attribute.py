"""Attribute Class."""

from copy import deepcopy
from ValueSet import ValueSet


class Attribute(object):
    """
    Class for Attribute i.e., set containing single elements, subsets
    or containuous ranges of integers or decimals.

    attributes:
    label: name of Attribute (e.g. size), always a string
    value_set: set of values that the attribute can take on
    (e.g {small,large}) taken as a list and parsed into the standard
    format defined by ValueSet class.
    """

    def __init__(self, label, value_set):
        """Initialize an Attribute object."""
        # type checking before anything
        if not isinstance(label, str):
            raise TypeError("l parameter must be a string")

        self._label = label
        self._is_Attribute = True

        if hasattr(value_set, "_is_ValueSet"):
            self._value_set = deepcopy(value_set)
            return
        if isinstance(value_set, list):
            self._value_set = ValueSet(value_set)
        else:
            raise TypeError('v parameter must be of type ValueSet or list')

    def __eq__(self, other):
        """
        Determine if self Attribute object is equivalent to other
        Attribute object.
        """

        label_condition = self._label == other._label
        value_condition = self._value_set == other._value_set

        if label_condition and value_condition:
            return True
        else:
            return False

    def __ne__(self, other):
        """Determine if this Attribute is not equivalent to other Attribute."""
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Overloaded + operator.

        Combine this Attribute and another Attribute, Relation,
        AttributeStructure into an AttributeStructure or combine it with an
        AttributeSystem.
        """

        from AttributeStructure import AttributeStructure
        from AttributeSystem import AttributeSystem
        # handle Attribute and Attribute addition
        if hasattr(other, "_is_Attribute"):
            return AttributeStructure(self, other)
        # handle Attribute and Relation addition
        elif hasattr(other, "_is_Relation"):
            return AttributeStructure(self, other)
        # handle Attribute and AttributeStructure addition
        elif hasattr(other, "_is_AttributeStructure"):
            params = other._attributes + other._relations.values()
            params.append(deepcopy(self))
            return AttributeStructure(*params)
        # handle Attribute and AttributeSystem addition
        elif hasattr(other, "_is_AttributeSystem"):
            astr = deepcopy(other._attribute_structure)
            astr += deepcopy(self)
            return AttributeSystem(astr, deepcopy(other._objects))
        else:
            raise TypeError(
                "Only Relation, Attribute, and AttributeStructure objects may "
                "be added to an Attribute object.")

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Attribute object."""
        return Attribute(deepcopy(self._label), deepcopy(self._value_set))

    def __str__(self):
        "human-readable representation of attribute; 'label: {...}'."
        return self._label + ': ' + '{' + ''.join(
            [str(i) + ',' for i in self._value_set])[:-1] + '}'

    def __repr__(self):
        """Machine readable string repr; same as __str__."""
        return "\"" + self.__str__() + "\""

    def _key(self):
        """Private key function for hashing."""
        # Tuple key; not a permanent solution
        return (self._label, str(self._value_set))

    def __hash__(self):
        """Hash implementation for set comparison of Attributes."""
        return hash(self._key())


def main():
    """Main method; quick testing."""
    a = Attribute("yo", ["333", "33333", "333", 4, True, "[3, [edd, d]]"])
    b = Attribute("yerboi", [])
    print a + b

if __name__ == "__main__":
    main()
