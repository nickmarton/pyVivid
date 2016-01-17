"""attribute module."""

from copy import deepcopy
from valueset import ValueSet


class Attribute(object):
    """
    Attribute Class, i.e., a finite set *A* with an associated label *l*.

    :ivar label: the associated label *l* of the Attribute *A*.
    :ivar value_set: the set of values that the attribute can take on \
    (e.g {small,large}).
    :ivar _is_Attribute: An identifier to use in place of type or isinstance.
    """

    def __init__(self, label, value_set):
        """
        Construct an Attribute object.

        :param label: The label *l* to associate with the Attribute object.
        :type  label: str

        :param value_set: The set of values the Attribute can take on.
        :type  value_set: list|ValueSet

        :raises TypeError: label parameter must be a string and value_set \
        parameter must be either a ValueSet object or a list.
        """

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
        Determine if two Attribute objects are equal via the ``==`` operator.
        """

        label_condition = self._label == other._label
        value_condition = self._value_set == other._value_set

        if label_condition and value_condition:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two Attribute objects are not equal via the ``!=`` operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Combine an Attribute object with another Attribute object, \
        a Relation object, an AttributeStructure object or an AttributeSystem \
        object via the ``+`` operator.

        :param other: The object to combine with the Attribute. \
        If an Attribute, Relation, or AttributeStructure object is provided, \
        an AttributeStructure object is returned; if an AttributeSystem \
        object is provided, an AttributeSystem is returned.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: other parameter must be an Attribute, Relation, \
        AttributeStructure, or AttributeSystem object.
        """

        from attribute_structure import AttributeStructure
        from attribute_system import AttributeSystem
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
        """
        Deepcopy an Attribute object via the ``copy.deepcopy`` method.
        """

        return Attribute(deepcopy(self._label), deepcopy(self._value_set))

    def __str__(self):
        "Return a readable string representation of the Attribute object with the \
        following form: \
        \"*label:* {v\ :sub:`1`\ , :math:`\ldots` ,v\ :sub:`n`\ }.\""
        return self._label + ': ' + '{' + ''.join(
            [str(i) + ',' for i in self._value_set])[:-1] + '}'

    def __repr__(self):
        "Return a string representation of the Attribute object with the \
        following form: \
        \"*label:* {v\ :sub:`1`\ , :math:`\ldots` ,v\ :sub:`n`\ }.\""
        return "\"" + self.__str__() + "\""

    def _key(self):
        """Private key function for hashing."""
        return (self._label, str(self._value_set))

    def __hash__(self):
        """Hash implementation for set functionality of Attribute objects."""
        return hash(self._key())


def main():
    """Main method; quick testing."""
    a = Attribute("yo", ["333", "33333", "333", 4, True, "[3, [edd, d]]"])
    b = Attribute("yerboi", [])
    print a + b

if __name__ == "__main__":
    main()
