"""Formula class."""

class Formula(): 
    """
    Class for a formula in respect to some Vocabulary sigma; 

    in our applications, a formula is a relation
    This class is intended to provide a skeleton for a computable
    function in accordance with some Vocabulary sigma.
    
    It is a skeleton in the sense that the definition of the formula,
    that is the expression that is computed is defined as follows:
    
    each formula is provided a name, which must match some relation 
    in a given Vocabulary. Then, each formula is nothing more than an
    object created for some relation symbol. 

    A Formula can only be evaluated through te assign_truth_value()
    function, which in turn requires a call to the 
    get_attribute_interpretation() which creates an interpretation 
    table. 
    
    By definition, the interpretation table contains an entry for each 
    relation symbol within some Vocabulary. Since the name of the 
    formula is the label of some relation symbol in a Vocabulary, 
    if it is not found in the interpretation table an error is thrown.

    As such, the members of each Formula object are as follows:

    sigma: the Vocabulary for which the formula will be valid; 
    we store a copy of the Vocabulary for convenience and error checking
    
    name: the name of the formula used as an identifier; 
    if the name is not in the Vocabulary sigma's relations, 
    an error is thrown
    
    terms: a list of terms (either constants or variables) 
    that are present in the formula; if every one of these in the list 
    are not contained by either the Vocabulary's constants C or 
    variables V, an error is thrown.
    """

    def __init__(self, vocabulary, name, *terms):
        if not isinstance(vocabulary, Vocabulary): 
            raise TypeError(vocabulary + " must be a Vocabulary object")
        if not isinstance(name, str): 
            raise TypeError(name + " must be a string")
        
        relation_symbol_names = [rs.get_name() for rs in vocabulary.get_R()]
        
        if name not in relation_symbol_names: 
            raise ValueError(
                "only definitions matching some Relation " +
                "in vocabulary supported at the moment"
                )
        if not terms : 
            raise ValueError("at least 1 term must be provided")                        #no terms, do not accept Formula with arity of 0
        
        for t in terms:                                                                 #for all terms provided
            
            if t in vocabulary.get_C() and t not in vocabulary.get_V(): c1 = True                 #if term is in C but not V
            else: c1 = False
            if t not in vocabulary.get_C() and t in vocabulary.get_V(): c2 = True                 #if term is in V but not C
            else: c2 = False
            
            if not c1 and not c2:                                                       #if not (c1 or c2); that is if not(C XOR V)
                raise ValueError(                                                       #raise exception, 
                    "all terms must be contained in Vocabulary" +                       #we only want to allow the same term to be present in C or V but not both
                    " in C XOR V"
                    )           
        
        self._vocabulary = vocabulary
        self._name = name
        self._terms = list(terms);

    def __eq__(self, other):
        if self._vocabulary == other._vocabulary and self._name == other._name and\
         self._terms == other._terms: return True
        else: return False
    
    def __ne__(self, other):
        if self._vocabulary == other._vocabulary and self._name == other._name and\
         self._terms == other._terms: return False
        else: return True

    def __repr__(self): return self.get_name()

    def get_vocabulary(self): return self._vocabulary
    
    def set_vocabulary(self, s):
        """
        Replace self.vocabulary with s; 

        s must contain the self._name and all t in self._terms for this
        to be a successful call
        """

        if isinstance(s, Vocabulary):                                                   #if s is a Vocabulary
            if self.get_name() in s.get_R():                                            #and s contains the relation that formula holds
                for t in self.get_terms(): 
                    
                    if t in vocabulary.get_C() and t not in vocabulary.get_V(): c1 = True         #if term is in C but not V
                    else: c1 = False
                    if t not in vocabulary.get_C() and t in vocabulary.get_V(): c2 = True         #if term is in V but not C
                    else: c2 = False
                    
                    if not c1 and not c2:                                               #if not (c1 or c2); that is if not(C XOR V)
                        raise ValueError(                                               #raise exception, 
                            "all terms must be contained in Vocabulary" +               #we only want to allow the same term to be present in C or V but not both
                            "in C XOR V"
                            )

                self._vocabulary = s                                                         #name and all terms in s, set self._vocabulary to s
            else:raise ValueError("s must contain " + self.get_name())                  #s does not have formula's relation, raise ValueError
    
    def get_name(self): return self._name
    
    def set_name(self, r):
        """
        replace self._name with r; 
        
        r must be contained in self.vocabulary._r for this to be a 
        successful call."""
        
        if isinstance(r, str):                                                      #if r is a string
            if r in self.get_vocabulary().get_R():                                           #if r is in Vocabulary's relations
                self._name = r
            else: raise ValueError(r + "must be contained in " + vocabulary)
        else: raise ValueError("r must be a string")
    
    def get_terms(self): return self._terms
    
    def set_terms(self, *terms):
        """
        Set self._terms to terms;
        
        terms must contain at least 1 term and all terms must be 
        contained in Vocabulary.
        """
        
        if not terms: raise ValueError("at least 1 term must be provided")
        for t in terms:                                                             #for all terms provided
            if t in vocabulary.get_C() and t not in vocabulary.get_V(): c1 = True                 #if term is in C but not V
            else: c1 = False
            if t not in vocabulary.get_C() and t in vocabulary.get_V(): c2 = True                 #if term is in V but not C
            else: c2 = False
            
            if not c1 and not c2:                                                       #if not (c1 or c2); that is if not(C XOR V)
                raise ValueError(                                                       #raise exception, 
                    "all terms must be contained in Vocabulary" +                       #we only want to allow the same term to be present in C or V but not both
                    "in C XOR V"
                    )
        self._terms = list(terms)

    def __str__(self):
        return self.get_name() + '(' + ''.join(                                        #Start with name(
            [str(t) + ', ' for t in self.get_terms()]                                   #add all terms, separated by commas
            )\
            [:-2] + ')'                                                                #drop trailing ", " and add closing parenthesis 
