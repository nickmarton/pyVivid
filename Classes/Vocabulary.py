"""Vocabulary class."""

from assistance_functions import *

def prevent_duplicates(x, label):
    """Prevent duplicates in x by raising a ValueError."""

    for i, x1 in enumerate(x):                                                          #for every element x1 in x
        for j, x2 in enumerate(x):                                                      #for every element x2 in x
            if i != j:                                                                  #if x1 and x2 are different entries in x
                if x1 == x2:                                                            #if two different entries in x are equal
                    raise ValueError(                                                   #explicitly raise ValueError; forbid duplicate elements
                        'Duplicate ' + label + ' not ' +
                        'allowed in Vocabulary')   

class Vocabulary:
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

        if not isinstance(C, list):                                                 #if C parameter is not of type list
            raise TypeError(                                                            #explicitly raise TypeError
                'C parameter must be of type list'
                )
        if not isinstance(R, list):                                                 #if R parameter is not of type list
            raise TypeError(                                                            #explicitly raise TypeError
                'R parameter must be of type list'
                )
        if not isinstance(V, list):                                                 #if V parameter is not of type list
            raise TypeError(                                                            #explicitly raise TypeError
                'V parameter must be of type list'
                )
        
        for c in C:                                                                 #for every member c of C
            if not isinstance(c, str):                                                  #if c is not of type  string
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in C parameter must ' + 
                    'be of type str'
                    )   

        for rs in R:                                                                    #for every member rs of R
            if not isinstance(rs, RelationSymbol):                                 #if rs is not of type RelationSymbol
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in R parameter must ' + 
                    'be of type RelationSymbol'
                    )

        for v in V:                                                                 #for every member v of V
            if not isinstance(v, str):                                                  #if v is not of type  string
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in V parameter must ' + 
                    'be of type str'
                    )
        
        intersection = (set(C) & set(V))                                                #determine if C and V have any shared elements
        if len(intersection) > 0:                                                       #if C and V have a common element
            raise ValueError(                                                           #explicitly raise ValueError
                'C and V parameters may not have a common element')

        prevent_duplicates(C, 'constants')                                              #prevent duplicates in C
        prevent_duplicates(R, 'relation symbols')                                       #prevent duplicates in R
        prevent_duplicates(V, 'variables')                                              #prevent duplicates in V

        self._c = C
        self._r = R
        self._v = V

    def __eq__(self, other):
        """
        Return boolean for whether or not this Vocabulary is equal 
        to other; magic function used for easy equality i.e., 
        self == other.
        """
        
        #try to find one-to-one mapping of self._r to other._r; only need to check one side as lengths are the same and no duplicates allowed

        if len(self._r) == len(other._r):                                               #if R has the same length in both self and other
            for r1 in self._r:                                                          #for each RelationSymbol in R of self
                for r2 in other._r:                                                 #for each RelationSymbol in R of other
                    if r1 == r2:                                                        #if r1 has a match in r2
                        break                                                           #break from for-else
                else:                                                                   #no match found for r1 in r2
                    return False                                                        #not equal, return False
        else:                                                                           #if R's have different length
            return False                                                                #not equal, return False

        r = True                                                                        #condition 2, r's match; this is checked above

        if len(self._c) == len(other._c):                                               #if length of C's match
            if set(self._c) == set(other._c):                                           #if unordered lists are equivalent
                c = True                                                                #then C's match
            else:                                                                       #otherwise no 1-to-1 mapping
                c = False                                                               #C's don't match
        else:                                                                           #C lengths aren't the same
            c = False                                                                   #C's don't match

        if len(self._v) == len(other._v):                                               #if length of V's match
            if set(self._v) == set(other._v):                                           #if unordered lists are equivalent
                v = True                                                                #then V's match
            else:                                                                       #otherwise no 1-to-1 mapping
                v = False                                                               #V's don't match
        else:                                                                           #V lengths aren't the same
            v = False                                                                   #V's don't match
        
        if c and r and v:                                                               #if all 3 conditions met, they are equal
            return True                                                                 #return True
        else:                                                                           #some component in self isn't equal to its counterpart in other
            return False                                                                #return False
    
    def __ne__(self, other):
        """
        Return boolean for whether or not this Vocabulary is not 
        equal to other; magic function used for easy equality i.e.,
        self != other.
        """
        
        #try to find one-to-one mapping of self._r to other._r; only need to check one side as lengths are the same and no duplicates allowed

        if len(self._r) == len(other._r):                                               #if R has the same length in both self and other
            for r1 in self._r:                                                          #for each RelationSymbol in R of self
                for r2 in other._r:                                                 #for each RelationSymbol in R of other
                    if r1 == r2:                                                        #if r1 has a match in r2
                        break                                                           #break from for-else
                else:                                                                   #no match found for r1 in r2
                    return True                                                         #not equal, return True
        else:                                                                           #if R's have differnet length
            return True                                                                 #not equal, return True
        
        r = True                                                                        #condition 2, r's match; this is checked above

        if len(self._c) == len(other._c):                                               #if length of C's match
            if set(self._c) == set(other._c):                                           #if unordered lists are equivalent
                c = True                                                                #then C's match
            else:                                                                       #otherwise no 1-to-1 mapping
                c = False                                                               #C's don't match
        else:                                                                           #C lengths aren't the same
            c = False                                                                   #C's don't match

        if len(self._v) == len(other._v):                                               #if length of V's match
            if set(self._v) == set(other._v):                                           #if unordered lists are equivalent
                v = True                                                                #then V's match
            else:                                                                       #otherwise no 1-to-1 mapping
                v = False                                                               #V's don't match
        else:                                                                           #V lengths aren't the same
            v = False                                                                   #V's don't match
        
        if not c or not r or not v:                                                     #some component in self isn't equal to its counterpart in other
            return True                                                                 #return True
        else:                                                                           #all components equal
            return False                                                                #return False

    def deep_copy(self):
        """Return a deep copy of this Vocabulary object."""
        import copy

        c_copy = copy.copy(self._c)
        r_copy = copy.deepcopy(self._r)
        v_copy = copy.copy(self._v)

        return Vocabulary(c_copy, r_copy, v_copy)

    def constant_assignment(self, objs): 
        """
        Create a partial or total constant assignment from 
        vocab.C to objs.
        """
        
        if not isinstance(objs, list):                                              #enforce objs parameter as list
            raise TypeError(
                'objs parameter must be of type list'
                )
        
        return pygame_mapping(self.get_C(), objs)

    def variable_assignment(self, objs): 
        """
        Create a total constant assignment from vocab.V to objs.
        """
        
        if not isinstance(objs, list):                                              #enforce objs parameter as list
            raise TypeError(
                'objs parameter must be of type list'
                )
        
        return pygame_mapping(self.get_V(), objs)
        
    def check_conflict(self, p1, p2):
        """
        Return boolean for whether or not p2 is in conflict with p1 in
        respect to this Vocabulary.
        """

        dom1 = p1.get_domain()                                                      #grab Dom(p1)
        dom2 = p2.get_domain()                                                      #grab Dom(p2)
        intersection = list(set(dom1) & set(dom2))                                      #get intersection of Dom(p1) and Dom(p2)
        
        for c in intersection:
            if p1.get_mapping()[c] != p2.get_mapping()[c]: 
                return True                                                             #if any shared constants such that p1(c) != p2(c), conflict
        return False                                                                    #otherwise, n

    def __str__(self):
        c_str = '[' + ''.join([c + ', ' for c in self.get_C()])[:-2] + ']'
        r_str = '[' + ''.join([str(r) + ', ' for r in self.get_R()])[:-2] + ']'
        v_str = '[' + ''.join([v + ', ' for v in self.get_V()])[:-2] + ']'

        return '(' + c_str + ', ' + r_str + ', ' + v_str + ')'

    def __repr__(self):
        c_str = '[' + ''.join([c + ', ' for c in self.get_C()])[:-2] + ']'
        r_str = '[' + ''.join([str(r) + ', ' for r in self.get_R()])[:-2] + ']'
        v_str = '[' + ''.join([v + ', ' for v in self.get_V()])[:-2] + ']'

        return '(' + c_str + ', ' + r_str + ', ' + v_str + ')'


def main():
    """short tests."""
    

if __name__ == "__main__":
    main()