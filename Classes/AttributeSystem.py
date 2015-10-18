"""Attribute System class."""

from AttributeStructure import Attribute, Relation, AttributeStructure

class AttributeSystem(object):
    '''Class for Attribute System'''
    def __init__(self, A, objects):
        """Construct AttributeSystem object."""
        #Enforce objects as list of strings
        if not isinstance(objects, list):
            raise TypeError("objects parameter must be of type list")
        for obj in objects:
            if not isinstance(obj, str):
                raise TypeError(str(objects) + " must contain only strings")
        
        #Enforce AttributeStructure type
        if not hasattr(A, "_is_AttributeStructure"):
            raise TypeError("A parameter must be of type AttributeStructure")
        
        #enforce no duplicate objects
        if len(objects) != len(set(objects)):
            raise ValueError(
                "dupicate objects not allowed in AttributeSystem")

        #sort objects before setting them
        self._objects = sorted(objects)
        self._attribute_structure = A
        self._is_AttributeSystem = True

    def __eq__(self, other):
        """Implement == for AttributeSystem's."""
        c_astr = self._attribute_structure == other._attribute_structure
        c_objs = self._objects == other._objects
        if c_astr and c_objs:
            return True
        else:
            return False
    
    def __ne__(self, other):
        """Implement != for AttributeSystem's."""
        return not self.__eq__(other)

    def __deepcopy__(self):
        """Return a deep copy of this AttributeSystem object."""
        import copy
        objects_copy = copy.deepcopy(self._objects)
        attribute_structure_copy = copy.deepcopy(self._attribute_structure)
        return AttributeSystem(objects_copy, attribute_structure_copy)

    def get_power(self):
        """Get power of this AttributeSystem, i.e., n * |A|."""
        return len(self._objects) * self._attribute_structure.get_cardinality()

    def __str__(self):
        """Return human-readable string representation of AttributeSystem."""
        asys_str = '({' + ''.join([s_i + ', ' for s_i in self._objects])[:-2]
        asys_str += '} ; ' + str(self._attribute_structure) + ')'
        return asys_str

    def __repr__(self):
        """Machine representation of this AttributeSystem; same as str()."""
        return self.__str__()

    def is_automorphic(self):
        """Determine if Attribute System is automorphic."""
        #Check if any object is a subset of value set of any attribute
        for s in self._objects:
            for a in self._attribute_structure._attributes:
                if is_subset([s], a._value_set):
                    return True
        return False

def main():
    """Main method for quick tests."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"], 1)

    a = AttributeStructure(a, b, c, r)
    o = ['o3', 'o1', 'o5', 'o2', 'o4']

    asys = AttributeSystem(a, o)
    print str(asys)

if __name__ == "__main__":
    main()