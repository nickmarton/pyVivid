"""Attribute Class."""

from assistance_functions import parse, nested_equivalence

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

    def __init__(self, label, value_set):
        """
        Initialize an Attribute object; parse the value set
        (v parameter) according to parse provided within the kernel.
        """

        #type checking before anything
        if not isinstance(label, str):
            raise TypeError("l parameter must be a string")
        if not isinstance(value_set, list):
            raise TypeError('v parameter must be of type list')

        self._label = label
        self._value_set = parse(value_set)

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
        return not self.__eq__(other)

    def set_label(self, label):
        """Set label to exclusively strings."""
        if not isinstance(label, str): raise TypeError("label must be string")
        else: self._label = label
    
    def get_label(self):
        """Get attribute label."""
        return self._label
    
    def set_possible_values(self, value_set): 
        """
        Set value set it's a list; raise TypeError it's not.
        Must be a list and parsable.
        """

        if not isinstance(value_set, list): 
            raise TypeError('Possible values must be stored in a list')
        else: 
            self._value_set = parse(value_set)    
    
    def get_possible_values(self): 
        """Return this Attribute object's value set."""
        return self._value_set

    def __str__(self):
        "human-readable representation of attribute; 'label: {...}''."
        return self._label + ': ' + '{' + ''.join(
            [str(i) + ',' for i in self._value_set])[:-1] + '}'

    def __repr__(self):
        """Machine readable string repr; same as __str__."""
        return "\"" + self.__str__() + "\""

def main():
    """Main method; quick testing."""
    a = Attribute("yo", ["333", "33333", "333", 4, True, "[3, [edd, d]]"])
    print a != a

if __name__ == "__main__":
    main()