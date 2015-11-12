"""Vocabulary class."""

from RelationSymbol import RelationSymbol

class Vocabulary(object):
    """
    Class for First-Order Vocabulary
        
    C: Constants; can be either partially or totally mapped to 
    {s1,...,sn}
    R: Relation Symbols, each with unique positive arity
    V: Vairables; can be totally mapped to {s1,...,sn}

    TypeError's are raised if C, R, or V are of type list
    TypeError is raised if all members of R list are not of type
    RelationSymbol.
    """

    def __init__(self, C, R, V):
        """
        Initialize Vocabulary object with lists of constants C, list of
        Relation_Symbols R, and list of variables V

        Raise TypeError if C, R, or V are not lists and if R contains 
        anything other than RelationSymbol objects.
        """

        if not isinstance(C, list):
            raise TypeError('C parameter must be of type list')
        if not isinstance(R, list):
            raise TypeError('R parameter must be of type list')
        if not isinstance(V, list):
            raise TypeError('V parameter must be of type list')
        
        for c in C:
            if not isinstance(c, str):
                raise TypeError(
                    'all entries in C parameter must be of type str')

        for rs in R:
            if not isinstance(rs, RelationSymbol):
                raise TypeError(
                    'all entries in R parameter must be of type RelationSymbol')

        for v in V:
            if not isinstance(v, str):
                raise TypeError(
                    'all entries in V parameter must be of type str')
        
        intersection = (set(C) & set(V))
        if len(intersection) > 0:
            raise ValueError(
                'C and V parameters may not have a common element')

        self._C = sorted(list(set(C)), key=lambda c: c.lower())
        self._R = sorted(list(set(R)), key=lambda rs: rs._name.lower())
        self._V = sorted(list(set(V)), key=lambda v: v.lower())
        self._is_Vocabulary = True

    def __eq__(self, other):
        """Implement == operator for Vocabulary object."""
        #constructor removes duplicates, so set comparison okay
        c_cond = set(self._C) == set(other._C)
        r_cond = set(self._R) == set(other._R)
        v_cond = set(self._V) == set(other._V)
        
        if c_cond and r_cond and v_cond:
            return True
        else:
            return False
    
    def __ne__(self, other):
        """Implement != operator for Vocabulary object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Vocabulary object."""
        from copy import deepcopy
        return Vocabulary(
            deepcopy(self._C), deepcopy(self._R), deepcopy(self._V))

    def add_constant(self, constant):
        """Add a constant to this Vocabulary object's C."""
        if type(constant) != str:
            raise TypeError("constant parameter must be a string")
        
        in_C = constant in self._C
        in_V = constant in self._V
        if not in_C and not in_V:
            self._C = sorted(self._C + [constant], key=lambda c: c.lower())
        else:
            raise ValueError("duplicate symbol cannot be added")

    def add_variable(self, variable):
        """Add a variable to this Vocabulary object's V."""
        if type(variable) != str:
            raise TypeError("variable parameter must be a string")
        
        in_C = variable in self._C
        in_V = variable in self._V
        if not in_C and not in_V:
            self._V = sorted(self._V + [variable], key=lambda v: v.lower())
        else:
            raise ValueError("duplicate symbol cannot be added")

    @staticmethod
    def constant_assignment(vocabulary, objs): 
        """
        Create a partial or total constant assignment from 
        vocab.C to objs.
        """
        if not isinstance(vocabulary, Vocabulary):
            raise TypeError("vocabulary parameter must be of type Vocabulary")

        if not isinstance(objs, list):
            raise TypeError('objs parameter must be of type list')
        
        return pygame_mapping(vocabulary.get_C(), objs)

    @staticmethod
    def variable_assignment(vocabulary, objs): 
        """
        Create a total constant assignment from vocab.V to objs.
        """
        if not isinstance(vocabulary, Vocabulary):
            raise TypeError("vocabulary parameter must be of type Vocabulary")

        if not isinstance(objs, list):
            raise TypeError('objs parameter must be of type list')
        
        return pygame_mapping(vocabulary.get_V(), objs)

    def _key(self):
        """Tuple key for hash function."""
        return (tuple(self._C), tuple(self._R), tuple(self._V))

    def __hash__(self):
        """Hash so sets can use Vocabulary's."""
        return hash(self._key())

    def __str__(self):
        """Implement str(Vocabulary)."""
        c_str = '[' + ''.join([c + ', ' for c in self._C])[:-2] + ']'
        r_str = '[' + ''.join([str(r) + ', ' for r in self._R])[:-2] + ']'
        v_str = '[' + ''.join([v + ', ' for v in self._V])[:-2] + ']'

        return '(' + c_str + ', ' + r_str + ', ' + v_str + ')'

    def __repr__(self):
        """Implement repr(Vocabulary)."""
        return self.__str__()

def main():
    """short tests."""
    pass

if __name__ == "__main__":
    main()