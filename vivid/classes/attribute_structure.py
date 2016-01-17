"""attribute_structure module."""

from attribute import Attribute
from relation import Relation
from copy import deepcopy
from functools import total_ordering


@total_ordering
class AttributeStructure(Attribute):
    """
    AttributeStructure class composed of Attribute and Relation objects,
    i.e., :math:`\mathcal{A}` = ({*A*\ :sub:`1`\, :math:`\ldots` , \
    *A*\ :sub:`k`\}; :math:`\mathcal{R}`)

    The AttributeStructure class uses the ``total_ordering`` decorator so
    strict subsets, supersets and strict supersets are also available via the
    ``<``, ``>=``, and ``>`` operators respectively, despite the lack of magic
    functions for them.

    :ivar attributes: list of Attribute objects (i.e., {*A*\ :sub:`1`\, \
    :math:`\ldots` , *A*\ :sub:`k`\}); always maintained as a list
    :ivar relations: dictionary of relations (i.e., :math:`\mathcal{R}`).
    :ivar _is_AttributeStructure: An identifier to use in place of type or \
    isinstance.
    """

    def __init__(self, *args):
        """
        Construct an AttributeStructure object.

        :param args: Attribute or Relation objects.
        :type  args: Attribute|Relation

        :raises TypeError: all optional positional arguments must be \
        Attribute or Relation objects.
        :raises ValueError: Duplicate Attribute labels are not permitted, \
        Duplicate Relation subscripts are not permitted, and each Relation's \
        *D*\(*R*\) must be a subset of the cartesian product of some \
        combination of the labels of the Attributes provided.
        """

        self._attributes = []
        self._relations = {}
        self._is_AttributeStructure = True

        a_ops, r_ops = [], []
        for op in args:
            if hasattr(op, "_is_Attribute"):
                a_ops.append(op)
            elif hasattr(op, "_is_Relation"):
                r_ops.append(op)
            else:
                # op is not Attribute or Relation, raise TypeError
                raise TypeError(
                    "all optional positional arguments must be of type "
                    "Attribute or Relation")

        # Sort provided (copy of) args so that attributes are added first
        sorted_a_ops = sorted(a_ops, key=lambda x: x._label)
        sorted_r_ops = sorted(r_ops, key=lambda x: x._subscript)

        sorted_ops = sorted_a_ops + sorted_r_ops

        # for each optional positional argument op
        for op in sorted_ops:
            # if op is an Attribute
            if hasattr(op, "_is_Attribute"):
                # if attribute is not a duplicate add attribute to objects list
                # of attributes
                if op not in self._attributes:
                    self._attributes.append(op)
                else:
                    raise ValueError(
                        "Duplicate labels are not permitted")

            # if op is a Relation
            elif hasattr(op, "_is_Relation"):

                # prevent duplicate subscripts
                if op._subscript in self._relations.keys():
                    raise ValueError(
                        "Duplicate subscripts not permitted in "
                        "AttributeStructure.")

                # if D(R) is within cartesian product of attribute labels
                if set(op.get_DR()) <= set(self.get_labels()):
                    # add op to object's relation dict
                    self._relations[op._subscript] = op
                    # start at top of loop to not raise exception
                    continue
                # op's D(R) is invalid, raise ValueError
                else:
                    raise ValueError(
                        "D(R) must be a subset of cartesian product "
                        "of some combination of attributes")

    def __eq__(self, other):
        """
        Determine if two AttributeStructure objects are equal via the ``==``
        operator.
        """

        # Attribute sets different length, not equal
        if len(self._attributes) != len(other._attributes):
            return False
        else:
            for i in range(len(self._attributes)):
                # Attributes not equal
                if self._attributes[i] != other._attributes[i]:
                    return False

        s_keys, o_keys = self._relations.keys(), other._relations.keys()
        # Different amount of relations, not equal
        if len(s_keys) != len(o_keys):
            return False
        for s_key in s_keys:
            for o_key in o_keys:
                if self._relations[s_key] == other._relations[o_key]:
                    break
            # No match for a relation found, not equal
            else:
                return False
        # Relations and Attributes are equal, structures are equal
        return True

    def __le__(self, other):
        """
        Overloaded ``<=`` operator. Determine if this AttributeStructure is a
        subset of other.
        """

        c_attribute = set(self._attributes) <= set(other._attributes)
        c_relation = self._relations <= other._relations

        return c_attribute and c_relation

    def __ne__(self, other):
        """
        Determine if two AttributeStructure objects are equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Add an Attribute, Relation, or AttributeStructure object via the ``+``
        operator.

        :param other: The object to combine with the AttributeStructure. \
        If an Attribute, Relation, or AttributeStructure object is provided, \
        an AttributeStructure object is returned; if an AttributeSystem \
        object is provided, an AttributeSystem is returned.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        Relation, AttributeStructure, or AttributeSystem object.
        :raises ValueError: Duplicate Attribute labels not permitted, \
        duplicate subscripts are not permitted and every Relation's \
        *D*\(*R*\) must be a subset of Attribute labels in the \
        AttributeStructure.
        """

        from attribute_system import AttributeSystem
        new_astr = deepcopy(self)

        # handle adding Attribute's to this AttributeStructure
        if hasattr(other, "_is_Attribute"):
            # Add other Attribute if it's label isn't in this
            # AttributeStructure
            if other._label not in self.get_labels():
                new_astr._attributes.append(deepcopy(other))
            else:
                raise ValueError(
                    "Duplicate Attribute objects not permitted")

        # handle adding Relation's to this AttributeStructure
        elif hasattr(other, "_is_Relation"):
            # if other Relation has a duplicate subscript raise ValueError
            if other._subscript in self._relations.keys():
                raise ValueError(
                    "Duplicate subscripts not permitted.")

            # check if other Relation's D(R) is a subset of this
            # AttributeStructure's Attribute labels
            if set(other._DR) <= set(self.get_labels()):
                new_astr._relations[other._subscript] = deepcopy(other)
            else:
                raise ValueError(
                    "operand must have all members of D(R) in this "
                    "AttributeStructure's attribute labels.")

        # handle adding AttributeStructure to this AttributeStructure
        elif hasattr(other, "_is_AttributeStructure"):
            for attribute in other._attributes:
                new_astr += deepcopy(attribute)
            for relation in other._relations.values():
                new_astr += deepcopy(relation)

        # handle adding AttributeSystem to this AttributeSystem
        elif hasattr(other, "_is_AttributeSystem"):
            astr = deepcopy(other._attribute_structure)
            objs = deepcopy(other._objects)

            new_astr = astr + deepcopy(self)
            return AttributeSystem(new_astr, objs)
        else:
            raise TypeError(
                "Only Relation, Attribute, AttributeStructure, and "
                "AttributeSystem objects can be added to an "
                "AttributeStructure.")

        return new_astr

    def __sub__(self, other):
        """
        Remove Attribute's or Relation's via ``-`` operator. If an
        AttributeStructure is provided, all Attributes and Relations within
        that AttributeStructure will be removed.

        :param other: The Attribute, Relation, or AttributeStructure to remove.
        :type  other: Attribute|Relation|AttributeStructure

        :raises KeyError: Invalid Relation provided.
        :raises TypeError: Only Attribute, Relation, or AttributeStructure \
        objects can be removed.
        :raises ValueError: Invalid Attribute provided if ``other`` is \
        Attribute, Relation or Attribute not contained in this \
        AttributeStructure if ``other`` is AttributeStructure or some \
        Relation's *D*\(*R*\) is invalid after Attribute removal.
        """

        # create copy before removing anything to not modify original
        copy = deepcopy(self)

        # Handle removal of Attribute from this AttributeStructure
        if hasattr(other, "_is_Attribute"):
            for i, attribute in enumerate(copy._attributes):
                if attribute._label == other._label:
                    del copy._attributes[i]
                    break
            else:
                raise ValueError(
                    "No attribute with label " + str(other._label))

        # Handle removal of Relation from this AttributeStructure
        elif hasattr(other, "_is_Relation"):
            if other._subscript not in copy._relations.keys():
                raise KeyError(
                    "No relation with subscript " + str(other._subscript))
            else:
                copy._relations.pop(other._subscript, None)

        # handle removal of AttributeStructure from this AttributeStructure
        elif hasattr(other, "_is_AttributeStructure"):

            # Determine if all attributes in other are in this
            # AttributeStructure
            attributes = set(copy._attributes)
            other_attributes = set(other._attributes)
            c_attribute = other_attributes <= attributes
            # Determine if all relations in other are in this
            # AttributeStructure
            c_relation = other._relations <= copy._relations

            if not c_attribute:
                raise ValueError(
                    "Attributes in right operand must be contained in left.")
            if not c_relation:
                raise ValueError(
                    "Relation in right operand must be contained in left")

            # remove Relations first for safety, then Attributes
            for relation in other._relations.values():
                copy -= relation
            for attribute in other._attributes:
                copy -= attribute
        else:
            raise TypeError(
                "Only Relation or Attribute objects can be removed to an "
                "AttributeStructure.")

        # extract what remains after successful removal and try to reconstruct
        ops = copy._attributes + copy._relations.values()
        try:
            return AttributeStructure(*ops)
        # catch case where AttributeStructure now has Relation(s) with some
        # D(R) that is no longer a subset of remaining Attribute's
        except ValueError:
            raise ValueError(
                "All remaining Relation D(R)'s after subtraction must be a "
                "subset of remaining Attribute's.")

    def __iadd__(self, other):
        """
        Add an Attribute, Relation, or AttributeStructure object via the ``+=``
        operator.

        :param other: The object to combine with the AttributeStructure. \
        If an Attribute, Relation, or AttributeStructure object is provided, \
        an AttributeStructure object is returned; if an AttributeSystem \
        object is provided, an AttributeSystem is returned.
        :type  other: Attribute|Relation|AttributeStructure|AttributeSystem

        :raises TypeError: other parameter must be an Attribute, Relation, \
        AttributeStructure, or AttributeSystem object.
        :raises ValueError: Duplicate Attribute labels not permitted, \
        duplicate subscripts are not permitted and every Relation's \
        *D*\(*R*\) must be a subset of Attribute labels in the \
        AttributeStructure.
        """

        return self.__add__(other)

    def __isub__(self, other):
        """
        Remove Attribute's or Relation's via ``-=`` operator. If an
        AttributeStructure is provided, all Attributes and Relations within
        that AttributeStructure will be removed.

        :param other: The Attribute, Relation, or AttributeStructure to remove.
        :type  other: Attribute|Relation|AttributeStructure

        :raises KeyError: Invalid Relation provided.
        :raises TypeError: Only Attribute, Relation, or AttributeStructure \
        objects can be removed.
        :raises ValueError: Invalid Attribute provided if ``other`` is \
        Attribute, Relation or Attribute not contained in this \
        AttributeStructure if ``other`` is AttributeStructure or some \
        Relation's *D*\(*R*\) is invalid after Attribute removal.
        """

        return self.__sub__(other)

    def __getitem__(self, key):
        """
        Retrieve a reference to the Attribute or Relation in the
        AttributeStructure via the key provided.

        :param key: The Attribute, Relation, label, or subscript to use when \
        attempting to find the cooresponding Attribute or Relation.
        :type  key: Attribute|Relation|str|int

        :raises KeyError: Attribute or Relation provided in ``key`` not found \
        in AttributeStructure or no Relation with subscript provided in \
        ``key`` found in AttributeStructure.
        :raises TypeError: ``key`` is not an Attribute, Relation, int, or str.
        :raises ValueError: no Attribute has label provided in ``key`` or \
        no Relation has subscript provided in ``key``.
        """

        # Handle index attempt with Attribute object
        if hasattr(key, "_is_Attribute"):
            for attribute in self._attributes:
                if attribute == key:
                    return attribute
            raise KeyError("No Attribute " + str(key) + " found.")

        # Handle index attempt with Relation object
        if hasattr(key, "_is_Relation"):
            for subscript, relation in self._relations.iteritems():
                if key == relation:
                    return relation
            raise KeyError("No Attribute " + str(key) + " found.")

        # Handle index attempt with string
        if isinstance(key, str):
            for attribute in self._attributes:
                if attribute._label == key:
                    return attribute
            import re
            if re.match(r'^R\d+$', key):
                subscript = int(key[1:])
                try:
                    return self._relations[subscript]
                except:
                    pass
            raise ValueError(
                "No Attribute(Relation) found with label(subscript): " + key)
        elif isinstance(key, int):
            try:
                return self._relations[key]
            except KeyError:
                raise KeyError(str(key) + " is not a valid Relation subscript")
        else:
            raise TypeError(
                "Only Attribute's, Relation's, strings, and ints can be used "
                "as an index")

    def __contains__(self, key):
        """
        Determine if Attribute, Relation, Attribute corresponding to label in
        ``key`` or Relation corresponding to subscript in ``key`` is contained
        by AttributeStructure via ``in`` operator.

        :param key: The key to use when checking for membership.
        :type  key: Attribute|Relation|str|int

        :raises TypeError: ``key`` must be an Attribute object, \
        Relation object, ``str``, or ``int``.
        """

        # Check if Attribute is within this AttributeStructure
        if hasattr(key, "_is_Attribute"):
            for attribute in self._attributes:
                if attribute == key:
                    return True
            return False

        # Check if Relation is within this AttributeStructure
        if hasattr(key, "_is_Relation"):
            for subscript, relation in self._relations.iteritems():
                if key == relation:
                    return True
            return False

        # Check if string is a label within this AttributeStructure
        if isinstance(key, str):
            for attribute in self._attributes:
                if attribute._label == key:
                    return True
            return False

        # Check if int is a subscript within this AttributeStructure
        if isinstance(key, int):
            if key in self._relations.keys():
                return True
            else:
                return False

        raise TypeError(
            "Type mismatch; only Attribute's, Relation's and "
            "label(Rsubscript) strings can be tested for membership.")

    def __deepcopy__(self, memo):
        """
        Deepcopy an AttributeStructure object via the ``copy.deepcopy`` method.
        """

        import copy

        attributes_copy = copy.deepcopy(self._attributes)
        relations_copy = copy.deepcopy(self._relations).values()

        ops_copy = ([attribute for attribute in attributes_copy] +
                    [relation for relation in relations_copy])

        return AttributeStructure(*ops_copy)

    def get_labels(self):
        """Return labels of Attributes within this AttributeStructure."""
        return [a._label for a in self._attributes]

    def get_subscripts(self):
        """Return subscripts of Relations within this AttributeStructure."""
        return self._relations.keys()

    def get_cardinality(self):
        """Return cardinality of this AttributeStructure."""
        return len(self._attributes)

    def __str__(self):
        """
        Return a readable string representation of the AttributeStructure
        object.
        """

        # Build sorted list of subscripts each separated by a comma
        r_string = ''.join(
            ['R' + str(i) + ',' for i in sorted(
                [i for i in self._relations.keys()])])[:-1] + ')'
        # Add attributes string
        # (e.g. size: {(0,...,651)}, objs: {True,False}, )
        return_str = '('
        return_str += ''.join(
            [str(attr) + ', ' for attr in self._attributes])[:-2]
        return_str += ' ; ' + r_string
        return return_str

    def __repr__(self):
        """
        Return a string representation of the AttributeStructure
        object.
        """

        return self.__str__()


def main():
    """Main method; quick testing."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"], 1)

    astr = AttributeStructure()
    print astr + a + b + r

if __name__ == "__main__":
    main()
