"""AssumptionBase class."""

from Formula import Formula

class AssumptionBase(object):
    """
    Assumption base object.

    Essentially this class is a container for a finite set of Formulae 
    over the same Vocabulary.
    """

    def __init__(self, *formulae):
        """Construct an AssumptionBase object."""
        self._formulae = []

        if formulae:
            #Ensure all optional positional args are of type Formula.
            for f in formulae: 
                if not hasattr(f, "_is_Formula"): 
                    raise TypeError(
                        "all arguments passed to constructor must be a "
                        "Formula object")


            #check for same vocabulary condition and add formula to list
            vocabulary = formulae[0]._vocabulary
            names = [f._name for f in formulae]

            if len(names) != len(set(names)):
                raise ValueError("Duplicate Formula names not permitted")

            for f in formulae:
                if vocabulary != f._vocabulary:
                    raise ValueError(
                        "all formulae provided to constructor must share the "
                        "same Vocabulary")

                #ensure no duplicates
                if f not in self._formulae:
                    self._formulae.append(f)

        self._is_AssumptionBase = True

    def __eq__(self, other):
        """Implement != operator for AssumptionBase objects."""
        if not hasattr(other, "_is_AssumptionBase"):
            raise TypeError("Can only compare an AssumptionBase object with "
                "another AssumptionBase object")

        #Cardinalities must be the same.
        if len(self._formulae) != len(other._formulae): 
            return False
        
        #check if each formula in self has a match in other.
        for sf in self.get_formulae():
            for of in other.get_formulae():
                if sf == of: 
                    break
            else: 
                return False
        return True
    
    def __ne__(self, other):    
        """Implement != operator for AssumptionBase objects."""
        return not self.__eq__(other)

    def __iter__(self):
        """Add an interator to the class for easy formula access."""
        for formula in self._formulae:
            yield formula
    
    def set_formulae(self, *formulae):
        """
        Set self._formulae of assumption base to formulae if all 
        members of formulae are of type Formula.
        """
        
        f_set = []

        if formulae:
            #Ensure all provided arguments are of type Formula
            for f in formulae: 
                if not isinstance(f, Formula): 
                    raise TypeError(
                        "all arguments passed to set_formulae() "
                        "must be of type Formula"
                        )
            
            vocabulary = formulae[0].get_vocabulary()

            #Ensure all formlae provided share the same vocabulary
            for f in formulae:
                if vocabulary != f.get_vocabulary():
                    raise ValueError(
                        "all formulae provided to set_formulae()"
                        " must have the same vocabulary")

                #ensure no duplicates
                if f not in f_set:
                    f_set.append(f)

        self._formulae = f_set
    
    def add_formulae(self, *formulae):
        """
        Add all formulae passed to self._formulae if they're not
        already in it.

        Raise ValueError if formulae passed to add_formulae don't
        share the same vocabulary as formulae within this
        AssumptionBase.
        """ 
        
        if formulae:
            #Ensure all provided arguments are of type Formula
            for f in formulae:
                if not isinstance(f, Formula): 
                    raise TypeError(
                        "all arguments passed to add_formulae() "
                        "must be of type Formula"
                        )

            vocabulary = formulae[0].get_vocabulary()

            #check for same vocabulary condition and add formula to list
            for f in formulae:
                if vocabulary != f.get_vocabulary():
                    raise ValueError(
                        "all formulae provided to constructor "
                        "must have the same vocabulary")

                #ensure no duplicates
                if f not in self.get_formulae():
                    self._formulae.append(f)

    def add_formula(self, formula):
        """
        Add a single formula to self.add_formulae if not already in it.

        Raise ValueError if formula does not share the same vocabulary
        as the formulae in this AssumptionBase.
        """

        if not isinstance(f, Formula): 
            raise TypeError(
                "argument passed to add_formula() must be of type Formula"
                )
        
        if f not in self.get_formulae(): 
            if formula.get_vocabulary() == self.get_vocabulary():
                self._formulae.append(f)
            else:
                raise ValueError(
                    "formula parameter must share the same "
                    "vocabulary as this AssumptionBase")

    def __str__(self):
        return ''.join([str(f) + '\n' for f in self._formulae])[:-1]

def main():
    """Quick tests."""
    from RelationSymbol import RelationSymbol
    from Vocabulary import Vocabulary

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1')

    AssumptionBase(f1, f2)

    print hash(f1)
    print hash(f2)

if __name__ == "__main__":
    main()