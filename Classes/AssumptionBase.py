"""AssumptionBase class."""

class AssumptionBase():
    """
    Assumption base object.

    Essentially this class is a container for a finite set of Formulae 
    over the same Vocabulary.
    """

    def __init__(self, *formulae):
        """
        Initialize an AssumptionBase object to contain formulae.

        Raise TypeError if any optional positional argument is not of
        type Formula.
        Raise ValueError if all Formulae don't share the same 
        vocabulary.
        """
        
        self._formulae = []

        if formulae:

            #Ensure all optional positional args are of type Formula.
            for f in formulae: 
                if not isinstance(f, Formula): 
                    raise TypeError(
                        "all arguments passed to __init__()"
                        " must be type Formula")

            vocabulary = formulae[0].get_vocabulary()

            #check for same vocabulary condition and add formula to list
            for f in formulae:
                if vocabulary != f.get_vocabulary():
                    raise ValueError(
                        "all formulae provided to constructor"
                        " must have the same vocabulary")

                #ensure no duplicates
                if f not in self.get_formulae():
                    self._formulae.append(f)

    def __eq__(self, other):
        """
        Check if self == other where both are AssumptionBase objects.
        """
        
        #Cardinalities must be the same.
        if len(self.get_formulae()) != len(other.get_formulae()): 
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
        """
        Check if self != other where both are AssumptionBase objects.
        """
        
        #Cardinalities must be not the same.
        if len(self.get_formulae()) != len(other.get_formulae()): 
            return True
        
        #check if each formula in self doesn't have a match in other.
        for sf in self.get_formulae():
            for of in other.get_formulae():
                if sf == of: 
                    break
            else: 
                return True
        return False

    def __iter__(self):
        """Add an interator to the class for easy formula access."""
        for formula in self._formulae:
            yield formula

    def get_vocabulary(self):
        """
        Return the vocabulary used by all the formulae in this 
        AssumptionBase.

        Raise AttributeError if there are no formulae in this 
        AssumptionBase and thus no vocabulary.
        """

        formulae = self.get_formulae()

        if formulae:
            return formulae[0].get_vocabulary()
        else:
            raise AttributeError(
                'No vocabulary associated with this AssumptionBase')

    def get_formulae(self): 
        """Return the formulae of this AssumptionBase."""
        return self._formulae
    
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
