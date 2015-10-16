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

class RelationSymbol:
    """
    Class for Relation Symbols consisting of a name and an arity; 
    
    this class is intended to be a helper class for Vocabulary as later
    on airty is required in addition to a name of a relation in Vocabulary

    name: a string designating the name of the relation symbol.
    arity: an integer designating the arity of the relation symbol.
    """

    def __init__(self, name, arity):
        """Initialize a RelationSymbol object with name and arity."""

        if not isinstance(name, str):                                                   #Enforce name as a string
            raise TypeError(
                'name parameter must be of type str'
                )
        if not isinstance(arity, int):                                                  #Enforce arity as an integer
            raise TypeError(
                'arity parameter must be of type int'
                )
        self._name = name                                                               #simply set name attribute to name parameter provided
        self._arity = arity                                                             #simply set arity attribute to arity parameter provided

    def __eq__(self, other):                                                            #magic function for easy equality comparison
        """
        Return whether self == other where self and other are 
        RelationSymbol objects.
        """

        n = self._name == other._name                                                   #condition 1, names match
        a = self._arity == other._arity                                                 #condition 2, arities match
        if n and a:                                                                     #if name and arity match, they are equal
            return True                                                                 #return True
        else:                                                                           #name and arity don't match
            return False                                                                #return False

    def __ne__(self, other):                                                            #magic function for easy equality comparison
        """
        Return whether self != other where self and other are 
        RelationSymbol objects.
        """

        n = self._name == other._name                                                   #condition 1, names match
        a = self._arity == other._arity                                                 #condition 2, arities match
        if not n or not a:                                                          #if name and arity don't match, they are not equal
            return True                                                                 #return True
        else:                                                                           #name and arity match
            return False                                                                #return False

    def get_name(self):
        """Return name of this RelationSymbol object."""

        return self._name

    def set_name(self, name):
        """
        Set name of this RelationSymbol object to name 
        parameter; raise TypeError if name parameter is not a string.
        """

        if not isinstance(name, str):                                                   #Enforce name as a string
            raise TypeError(
                'name parameter must be of type str'
                )
        else:                                                                           #provided name parameter is an string, set objects name to it
            self._name = name

    def get_arity(self):
        """Return arity of this RelationSymbol object.""" 

        return self._arity

    def set_arity(self, arity): 
        """
        Set arity of this RelationSymbol object to arity parameter;
        raise TypeError if arity parameter is not an int.
        """

        if not isinstance(arity, int):                                                  #Enforce arity as an int
            raise TypeError(
                'arity parameter must be of type int'
                )
        else:                                                                           #provided arity parameter is an int, set objects arity to it
            self._arity = arity

    def __str__(self): 
        """
        Return a string representation of this RelationSymbol
        object to the user for easy printing.
        """

        return self._name                                                               #simply return name; this will make mapping easier

    def __repr__(self): 
        """
        Return a string representation of this RelationSymbol
        object to the os for easy printing.
        """

        return self._name                                                               #simply return name; this will make mapping easier


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

    def get_C(self): 
        """Return Vocabulary's constants C."""

        return self._c
    
    def set_C(self, C): 
        """
        Set constants of vocabulary. 
        
        Raise TypeError if C is not a list of strings.
        Raise ValueError if C shares an element with V.
        """

        if not isinstance(C, list):                                                 #if C is not of type list 
            raise TypeError(                                                            #explicitly raise TypeError
            'C parameter must be of type list'
            )
        
        for c in C:                                                                 #for every member c of C
            if not isinstance(c, str):                                                  #if c is not of type  string
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in C parameter must ' + 
                    'be of type str'
                    )

        intersection = (set(C) & set(self.get_V()))                                     #determine if C and V have any shared elements
        if len(intersection) > 0:                                                       #if C and V have a common element
            raise ValueError(                                                           #explicitly raise ValueError
                'C and V parameters may not have a common element')

        prevent_duplicates(C, 'constants')                                              #prevent duplicates in C
        self._c = C

    def get_R(self): 
        """Return Vocabulary's Relation_Symbols R."""
        
        return self._r
    
    def set_R(self, R):
        """
        Set Relation_Symbols of Vocabulary.
        raise TypeError if R is not a list of Relation_Symbols.
        """

        if not isinstance(R, list):                                                 #if R is not of type list  
            raise TypeError(                                                            #explicitly raise TypeError
                'R parameter must be of type list'
                )

        for rs in R:                                                                    #for every member rs of R
            if not isinstance(rs, RelationSymbol):                                 #if rs is not of type RelationSymbol
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in R parameter must ' + 
                    'be of type RelationSymbol'
                    )
        
        prevent_duplicates(R, 'relation symbols')                                       #prevent duplicates in R
        self._r = R
            
    def get_V(self): 
        """Return Vocabulary's variables V."""

        return self._v
    
    def set_V(self, V): 
        """
        Set variables of Vocabulary.
        
        Raise TypeError if V is not a list of strings.
        Raise ValueError if V shares an element with C.
        """

        if not isinstance(V,list):                                                      #if V is not of type list
            raise TypeError(                                                            #explicitly raise TypeError
                'C parameter must be of type list'
                )  
        
        for v in V:                                                                 #for every member v of V
            if not isinstance(v, str):                                                  #if v is not of type  string
                raise TypeError(                                                        #explicitly raise TypeError
                    'all entries in V parameter must ' + 
                    'be of type str'
                    )

        intersection = (set(self.get_C()) & set(V))                                     #determine if C and V have any shared elements
        if len(intersection) > 0:                                                       #if C and V have a common element
            raise ValueError(                                                           #explicitly raise ValueError
                'C and V parameters may not have a common element')

        prevent_duplicates(V, 'variables')                                              #prevent duplicates in V
        self._v = V

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
