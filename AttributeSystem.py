"""Attribute System class."""

class AttributeSystem:
    '''Class for Attribute System'''
    def __init__(self, objs, A):
        if not isinstance(objs, list):                                                  #Raise TypeError if objs is not a list
            raise TypeError("objs parameter must be of type list")
        if not isinstance(A, AttributeStructure):                                              #Raise TypeError if A is not an AttributeStructure
            raise TypeError("A parameter must be of type AttributeStructure")
        
        if len(objs) != len(set(objs)):
            raise ValueError(
                "dupicate objects not allowed in AttributeSystem")

        self._objects = objs
        self._attribute_structure = A

    def __eq__(self, other):
        if self._attribute_structure == other._attribute_structure and \
        self._objects == other._objects: return True
        else: return False
    
    def __ne__(self, other):
        if self._attribute_structure != other._attribute_structure or \
        self._objects != other._objects: return True
        else: return False

    def deep_copy(self):
        """Return a deep copy of this AttributeSystem object."""

        import copy

        objects_copy = copy.copy(self._objects)
        attribute_structure_copy = self._attribute_structure.deep_copy()

        return AttributeSystem(objects_copy, attribute_structure_copy)

    def get_objects(self): return self._objects
    
    def set_objects(self, objs): 
        """Set objects of attribute system; raise TypeError if objs is not a list."""
        if not isinstance(objs, list): 
            raise TypeError('objs must be of type list')                                #Enforce objects as list
        
        if len(objs) != len(set(objs)):
            raise ValueError(
                "dupicate objects not allowed in AttributeSystem")

        self._objects = objs

    def get_attribute_structure(self): return self._attribute_structure
    
    def set_attribute_structure(self, A): 
        'Set attribute structure of attribute system; raise TypeError if A is not an Attribute Structure'
        if not isinstance(A, AttributeStructure):                                          #Enforce attribute structure as instance of AttributeStructure class
            raise TypeError('A must be of type AttributeStructure')
        else: self._attribute_structure = A

    def get_power(self):                                                                #Get power of system; n * |A|
        return len(self._objects) * self._attribute_structure.get_cardinality()

    def __str__(self):
        return '({' + ''.join(
            [s_i + ', ' for s_i in self._objects]                                       #list comprehension to build string for AttributeSystem's objects
            )\
            [:-2] + '} ; ' + str(self._attribute_structure) + ')'                               #drop trailing ", ", add attribute structure string and closing parenthesis

    def is_automorphic(self):
        'determine if Attribute System is automorphic'
        for s in self._objects:                                                     #suffices to check if any object is a subset of value set of any attribute
            for a in self.get_attribute_structure().get_attributes():
                if is_subset([s], a.get_possible_values()): return True
        return False
