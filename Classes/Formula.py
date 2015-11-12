"""Formula class; imutable."""

from RelationSymbol import RelationSymbol
from Vocabulary import Vocabulary

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
        """Construct a Formula object."""

        if not hasattr(vocabulary, "_is_Vocabulary"): 
            raise TypeError("vocabulary parameter must be a Vocabulary object")
        if type(name) != str: 
            raise TypeError(name + " must be a string")
        
        relation_symbol_names = [rs._name for rs in vocabulary._R]
        if name not in relation_symbol_names: 
            raise ValueError(
                "Name must match some RelationSymbol in Vocabulary")

        if not terms : 
            raise ValueError("at least 1 term must be provided")
        
        C, V = vocabulary._C, vocabulary._V

        for t in terms:
            
            if t in C:
                in_C = True
            else: 
                in_C = False
            if t in V:
                in_V = True
            else: 
                in_V = False

            #Vocabulary takes care of ensuring no overlap between C and V
            if not in_C and not in_V:
                raise ValueError(
                    "all terms must be contained in vocabulary's C or V")      
        
        from copy import deepcopy
        self._vocabulary = deepcopy(vocabulary)
        self._name = deepcopy(name)
        self._terms = list(terms);

    def __eq__(self, other):
        """Implement == operator for Formula."""
        vocab_cond = self._vocabulary == other._vocabulary
        name_cond = self._name == other._name
        terms_cond = self._terms == other._terms

        if vocab_cond and name_cond and terms_cond:
            return True
        else: 
            return False
    
    def __ne__(self, other):
        """Implement != operator for Formula object."""
        return not self.__eq__(other)

    def __str__(self):
        """Implement str(Formula)."""
        return self._name + '(' + ', '.join([str(t) for t in self._terms]) + ')'

    def __repr__(self):
        """Implement repr(Formula)."""
        return self.__str__()

def main():
    """Quick tests."""
    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    print f

if __name__ == "__main__":
    main()