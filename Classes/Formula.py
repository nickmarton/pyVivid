"""Formula class; imutable."""

from RelationSymbol import RelationSymbol
from Vocabulary import Vocabulary

class Formula(object): 
    """Class for a formula in respect to some Vocabulary sigma."""

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

        if not terms: 
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
        self._terms = list(set(list(terms)))
        self._is_Formula = True

    def __eq__(self, other):
        """Implement == operator for Formula."""
        if not hasattr(other, "_is_Formula"):
            raise TypeError(
                "can only compare Formula object with another Formula object")

        vocab_cond = self._vocabulary == other._vocabulary
        name_cond = self._name == other._name
        terms_cond = set(self._terms) == set(other._terms)

        if vocab_cond and name_cond and terms_cond:
            return True
        else: 
            return False
    
    def __ne__(self, other):
        """Implement != operator for Formula object."""
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for formula object."""
        from copy import deepcopy
        return Formula(
            deepcopy(self._vocabulary),
            deepcopy(self._name),
            *self._terms)

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