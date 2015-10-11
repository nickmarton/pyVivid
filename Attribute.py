class Attribute:
    """
    Class for Attribute i.e., set containing single elements, subsets
    or containuous ranges of integers or decimals
    
    attributes:
    label: name of Attribute (e.g. size), always a string
    value_set: set of values that the attribute can take on 
    (e.g {small,large}) taken as a list and parsed into the standard
    format outlined in parse function within the kernel file.
    """

    def __init__(self, l, v):
        """
        Initialize an Attribute object; parse the value set
        (v parameter) according to parse provided within the kernel.
        """

        #type checking before anything
        if not isinstance(l, str):
            raise TypeError("l parameter must be a string")
        if not isinstance(v, list):
            raise TypeError('v parameter must be of type list')

        self._label = l
        self._value_set = parse(v)

    def __eq__(self, other):
        """
        Determine if self Attribute object is equivalent to other
        Attribute object.
        """
        
        label_condition = self._label == other._label
        value_condition = nested_equivalence(self._value_set, other._value_set)
        
        if label_condition and value_condition:
            return True
        else:
            return False
    
    def __ne__(self, other):
        """Determine if this Attribute is not equivalent to other Attribute."""
        return not self.__eq__(self, other)

    def set_label(self, l):
        """Set label to exclusively strings."""
        if not isinstance(l, str): raise TypeError("label must be string")
        else: self._label = l
    
    def get_label(self):
        """Get attribute label."""
        return self._label
    
    def set_possible_values(self, v): 
        """
        Set value set to v if v is a list; raise TypeError if v is not a list.
        Must be a list and parsable.
        """

        if not isinstance(v, list): 
            raise TypeError('Possible values must be stored in a list')
        else: 
            self._value_set = parse(v)    
    
    def get_possible_values(self): 
        """Return this Attribute object's value set."""
        return self._value_set

    def __str__(self):
        "human-readable representation of attribute; 'label: {...}''."
        return self._label + ': ' + '{' + ''.join(
            [str(i) + ',' for i in self._value_set])[:-1] + '}'

def main():
    """Main method; quick testing."""
    a = Attribute("yo", [])

if __name__ == "__main__":
    main()