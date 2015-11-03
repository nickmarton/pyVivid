"""Relation Symbol class."""

class RelationSymbol(object):
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