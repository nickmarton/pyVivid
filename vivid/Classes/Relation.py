"""Relation class."""

from copy import deepcopy

class Relation(object):
    """
    Class for relations in attribute structures
    definition:     string representation of definition with form
                    "Rn(a,b,c) <=> ..." where n is a positive integer;
                    whitespace is ignored.
    DR:             D(R) denotes set {A1,...,An}; held as a list of strings
                    corresponding to labels of some set of Attributes; no
                    assumptions are made on labels of Attributes.
    subscript:      subscript of relation; defaults to lowest possible untaken
                    positive integer.
    """

    def __init__(self, definition, D_of_r, subscript=0):
        """Initialize a Relation object."""

        # type enforcement
        if not isinstance(definition, str):
            raise TypeError("definition parameter must be of type str")
        if not isinstance(D_of_r, list):
            raise TypeError("D_of_r must be of type list")
        if not isinstance(subscript, int): 
            raise TypeError("s must be of type int")

        # enforce that definition of relation is valid; this becomes important
        # when assign_truth_value() is called as the cardinality of the
        # arguments of R provided in the definition (e.g. R(x1,x2)) are compared
        # to the cardinality of the pairs in a profile; thus these arguments
        # must be provided.
        if not Relation.is_valid_definition(definition):
            raise ValueError(
                "definition parameter must be of form 'R(x1,x2,...,xn) <=> ' "
                "(with arbitrary whitespace allowed")

        # we have a valid definition, so grab the arguments from the definition
        # and count them
        params = definition[definition.find('(')+1: definition.find(')')]
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
        """Determine if two Relation objects are equal."""
        c_def = self._definition == other._definition
        c_DR = self._DR == other._DR
        c_subscript = self._subscript == other._subscript

        if c_def and c_DR and c_subscript:
            return True
        else: 
            return False

    def __ne__(self, other):
        """Determine if two Relation objects are not equal."""
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Overloaded + operator. 
        
        Combine this Attribute and another Attribute or Relation into an
        AttributeStructure.
        """

        from Attribute import Attribute
        from AttributeStructure import AttributeStructure
        from AttributeSystem import AttributeSystem
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
                "Only Relation or Attribute objects may be added to a "
                "Relation object.")

    def __iadd__(self, other):
        """Overload += operator."""
        return self.__add__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Relation object."""
        return Relation(
            str(self._definition), 
            deepcopy(self._DR), 
            int(self._subscript))

    def __str__(self):
        """Make human readable string of this Relation object."""
        return 'R' + str(self._subscript) + ' is a subset of ' + \
        self.get_DR(True) + ', defined as follows: ' + self._definition

    def __repr__(self):
        """Return machine representation of this Relation object; just RN."""
        return 'R' + str(self._subscript)
    
    def set_definition(self, definition):
        """Set definition; ensure that it conforms to required format."""
        if not isinstance(definition, str):
            raise TypeError("definition must be of type str")

        if Relation.is_valid_definition(definition):
            self._definition = definition
        else: 
            raise ValueError(
                "definition parameter must be of form 'R(x1,x2,...,xn) <=> ' "
                "(with arbitrary whitespace allowed")
    
    def get_DR(self, string=False): 
        """
        Return D(R) of relation. 
        If string is set to True, return string representation of D(R).
        """
        
        if string: return ''.join([l + ' X ' for l in self._DR])[:-3]
        else: 
            return self._DR
    
    def set_DR(self, DR): 
        """
        Set D(R); must be a list. 
        Raise TypeError if D(R) is not a list of strngs.
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
        arg_string = self._definition[start_paren+1:end_paren]
        r_args = arg_string.split(',')

        if len(r_args) != len(DR):
            raise ValueError(
                "D(R) cardinality must match definition argument cardinality")

        self._DR = DR

    def get_arity(self):
        """Return arity of this Relation object."""
        return len(self._DR)

    @staticmethod
    def is_valid_definition(definition):
        '''function to determine if a definition is valid
            A definition is valid when it is of the form R(x1,x2,...,xn) <=> <expression>
            The important thing here is the left hand side and the marker '<=>'. 
            Everything on the right hand side of '<=>' is ignored as far as Relation definition is concerned; 
            whether or not it is evaluatable is left to assign_truth_value() as it is only during the assignment
            of a truth value that the expression comes into play.
            All whitespace is trimmed immediately so arbitrary spacing is allowed.

            definition must be a string.
        '''
        wsf_definiton = "".join(definition.split())    # create whitespace free definition

        import re                                      # we will handle checking validity with regular expression

        matchObj = re.match(                           # we use match as it matches only the beginning of a string

            r'R' +                                     # begin with 'R'                             e.g. 'R'
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
                raise ValueError(
                    "duplicate arguments in relation not permitted")
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