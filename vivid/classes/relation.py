"""relation module."""

from copy import deepcopy


class Relation(object):
    """
    Relation class. Relation objects represent logical relations used in
    AttributeStructure objects.

    :ivar definition: A string representation of the Relation object's \
    definition with form ``Rn(a,...)<=>...`` where n is a positive integer; \
    whitespace is ignored.
    :ivar DR: DR represents :math:`D(R) \subseteq \{A_{1}, \ldots, A_{n}\}`; \
    held as a list of strings corresponding to the labels of some set of \
    Attributes objects; no assumptions are made on the labels of the \
    attributes.
    :ivar subscript: The subscript of the relation.
    :ivar _is_Relation: An identifier to use in place of ``type`` or \
    ``isinstance``.
    """

    def __init__(self, definition, D_of_r, subscript):
        """
        Construct a Relation object.

        :param definition: The definition of the logical relation; valid \
        definitions have the form: ``Rn(a,...) <=> ...`` where all whitespace \
        is ignored.
        :type  definition: str
        :param D_of_r: A list of strings representing \
        :math:`D(R) \subseteq \{A_{1}, \ldots, A_{n}\}`.
        :type  D_of_r: list
        :param subscript: The subscript of the relation; must match subscript \
        in definition.
        :type  subscript: int

        :raises TypeError: ``definition`` parameter must be a ``str``\, \
        ``D_of_r`` parameter must be a ``list`` containing only ``str``\s and \
        ``subscript`` parameter must be an ``int``\.
        :raises ValueError: ``definition`` parameter must be correctly \
        formatted, the number of parameters provided in ``definition`` must \
        match the length of ``D_of_r`` and ``subscript`` parameter must match \
        subscript provided in ``definition`` parameter.
        """

        # type enforcement
        if not isinstance(definition, str):
            raise TypeError("definition parameter must be of type str")
        if not isinstance(D_of_r, list):
            raise TypeError("D_of_r must be of type list")
        if not isinstance(subscript, int):
            raise TypeError("s must be of type int")

        # enforce that definition of relation is valid.
        if not Relation.is_valid_definition(definition):
            raise ValueError(
                "definition parameter must be of form 'R(x1,x2,...,xn) <=> ' "
                "(with arbitrary whitespace allowed")

        # we have a valid definition, so grab the arguments from the definition
        # and count them
        params = definition[definition.find('(') + 1: definition.find(')')]
        param_count = params.split(',')

        # if cardinality of parameters of definition provided doesn't match the
        # cardinality of D(R) raise a ValueError
        if len(param_count) != len(D_of_r):
            raise ValueError(
                "number of parameters provided in definition must match "
                "the cardinality of D(R), that is, the length of the "
                "D_of_r parameter")

        # ensure D_of_R has nothing but strings in it
        for label in D_of_r:
            if not isinstance(label, str):
                raise TypeError("D_of_R must contain only strings.")

        param_index = definition.find("(")
        definition_subscript = definition[1:param_index]

        if int(definition_subscript) != subscript:
            raise ValueError(
                "Subscript in definition must match subscript provided "
                "as argument")

        self._definition = definition
        self._DR = D_of_r
        self._subscript = subscript
        self._is_Relation = True

    def __eq__(self, other):
        """
        Determine if two Relation objects are equal via the ``==`` operator.
        """

        c_def = self._definition == other._definition
        c_DR = self._DR == other._DR
        c_subscript = self._subscript == other._subscript

        if c_def and c_DR and c_subscript:
            return True
        else:
            return False

    def __ne__(self, other):
        """
        Determine if two Relation objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Combine a Relation object with an Attribute object,
        an AttributeStructure object or an AttributeSystem object via the
        ``+`` operator.

        :param other: The object to combine with the Attribute. \
        If an Attribute or AttributeStructure object is provided, \
        an AttributeStructure object is returned; if an AttributeSystem \
        object is provided, an AttributeSystem is returned.
        :type  other: Attribute|AttributeStructure|AttributeSystem

        :raises TypeError: ``other`` parameter must be an Attribute, \
        AttributeStructure, or AttributeSystem object.
        """

        from attribute_structure import AttributeStructure
        from attribute_system import AttributeSystem
        # handle Relation and Attribute addition
        if hasattr(other, "_is_Attribute"):
            return AttributeStructure(self, other)
        # handle Relation and AttributeStructure addition
        elif hasattr(other, "_is_AttributeStructure"):
            params = other._attributes + other._relations.values()
            params.append(deepcopy(self))
            return AttributeStructure(*params)
        # handle Relation and AttributeSystem addition
        elif hasattr(other, "_is_AttributeSystem"):
            astr = deepcopy(other._attribute_structure)
            astr += deepcopy(self)
            return AttributeSystem(astr, deepcopy(other._objects))
        else:
            raise TypeError(
                "Only Attribute, AttributeStructure, or AttributeSystem "
                "objects may be added to a Relation object.")

    def __deepcopy__(self, memo):
        """
        Deepcopy a Relation object via the ``copy.deepcopy`` method.
        """

        return Relation(
            str(self._definition),
            deepcopy(self._DR),
            int(self._subscript))

    def __str__(self):
        """Return a readable string representation of the Relation object."""
        return 'R' + str(self._subscript) + ' is a subset of ' + \
            self.get_DR(True) + ', defined as follows: ' + self._definition

    def __repr__(self):
        """Return a string representation of the Relation object."""
        return 'R' + str(self._subscript)

    def set_definition(self, definition):
        """
        Set the definition of the Relation object to ``definition`` parameter
        after ensuring that it conforms to required format.

        :param definition: The new definition of the Relation object.
        :type  definition: str

        :raises TypeError: ``definition`` parameter must be a ``str``\.
        :raises ValueError: ``definition`` must conform to valid definition \
        rules.
        """

        if not isinstance(definition, str):
            raise TypeError("definition must be of type str")

        if Relation.is_valid_definition(definition):
            self._definition = definition
        else:
            raise ValueError(
                "definition parameter must be of form 'Rs(x1,x2,...,xn) <=> ' "
                "(with arbitrary whitespace allowed")

    def get_DR(self, string=False):
        """
        Return :math:`D(R)` of the calling Relation object. If ``string``
        parameter is set to True, return a ``str`` representation of
        :math:`D(R)`.

        :param string: A boolean value for whether or not to return a string \
        representation of :math:`D(R)`.
        :type  string: boolean

        :return: A representation of :math:`D(R)`.
        :rtype: ``str`` | ``list``
        """

        if string:
            return ''.join([l + ' X ' for l in self._DR])[:-3]
        else:
            return self._DR

    def set_DR(self, DR):
        """
        Set :math:`D(R)` to ``DR`` parameter.

        :param DR: The list of strings to set the calling Relation object's \
        :math:`D(R)` to.
        :type  DR: ``list``

        :raises TypeError: :math:`D(R)` is not a ``list`` of ``str``\s.
        :raises ValueError: The cardinality of :math:`D(R)` must match \
        argument cardinality in Relation object's definition member.
        """

        if not isinstance(DR, list):
            raise TypeError('D(R) must be a list')
        if not DR:
            raise TypeError('D(R) must be non-empty')
        for label in DR:
            if not isinstance(label, str):
                raise TypeError('D(R) must contain only strings')

        # get start and end parentheses
        start_paren = self._definition.find('(')
        end_paren = self._definition.find(')')

        # get arguments within definition e.g. R(a,b,c) -> [a, b, c]
        arg_string = self._definition[start_paren + 1:end_paren]
        r_args = arg_string.split(',')

        if len(r_args) != len(DR):
            raise ValueError(
                "D(R) cardinality must match definition argument cardinality")

        self._DR = DR

    def get_arity(self):
        """
        Return the arity of the calling Relation object.

        :return: The length of :math:`D(R)`.
        :rtype: ``int``
        """

        return len(self._DR)

    @staticmethod
    def is_valid_definition(definition):
        """
        Determine if a given definition in ``definition`` parameter is valid.
        A definition is valid when it is of the form
        ``Rs(x1,...,xn) <=>`` <expression>.

        The important thing here is the left hand side and the marker
        ``"<=>"``. Everything on the right hand side of ``"<=>"`` is ignored as
        far as the definition's validity is concerned; whether or not it is
        evaluatable is left to ``Formula.assign_truth_value()`` as it is only
        during the assignment of a truth value that the expression comes into
        play. All whitespace is trimmed immediately so arbitrary spacing is
        allowed.

        :param definition: The definition to verify.
        :type  definition: str

        :return: Whether or not ``definition`` is valid.
        :rtype: ``bool``
        """

        # Remove whitespace
        wsf_definiton = "".join(definition.split())

        import re

        matchObj = re.match(
            r'^R' +                                    # begin with 'R'                             e.g. 'R'
            '\d+' +                                    # followed by any whole numbers              e.g. 'R1'
            '\(' +                                     # then a '('                                 e.g. 'R1('
            '(\w+,)*' +                                # then 0 or more alphanumeric substrings     e.g. 'R1(h1,m1,h2,' or 'R1(' if only 1 argument
            '(\w+)' +                                  # then an alphanumeric substring             e.g. 'R1(h1,m1,h2,m2' or 'R1(h1' if only 1 argument
            '\)<=>',                                   # finished by ')<=>'                         e.g. 'R1(h1,m1,h2,m2)<=>' or 'R1(h1)<=>' if only 1 argument
            wsf_definiton)

        # if syntactially valid, determine if semantically valid
        if matchObj:

            # get start and end parentheses
            start_paren = definition.find('(')
            end_paren = definition.find(')')

            # get arguments within definition e.g. R(a,b,c) -> [a, b, c]
            arg_string = definition[start_paren + 1:end_paren]
            r_args = arg_string.split(',')

            # ensure no duplicate arguments
            if len(r_args) == len(set(r_args)):
                return True
            else:
                return False
        else:
            return False


def main():
    """Main method; quick testing."""
    r1 = Relation("R1(a) <=> ", ["a"], 0)
    r2 = Relation("R1(a) <=> ", ["a"], 0)

    print r1 + r2
    print type(r1 + r2)
if __name__ == "__main__":
    main()
