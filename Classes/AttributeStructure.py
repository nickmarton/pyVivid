"""Attribute Structure class."""

from Attribute import Attribute
from Relation import Relation
from copy import deepcopy

class AttributeStructure(Attribute):
    """
    Class for Attribute Structure composed of attributes and relations.
    
    attributes: list of attributes; always maintained as a list
    relations: dictionary of relations.
    """
    
    def __init__(self, *ops):
        """
        Initialize an AttributeStructure object.

        input:
        Attribute and Relation objects allowed in constructor in 
        arbitrary order via optional positional arguments.

        exceptions:
        A TypeError is raised if any of the optional positional 
        arguments provided are not of type Attribute or Relation.
        """

        self._attributes = []
        self._relations = {}
        self._is_AttributeStructure = True

        a_ops, r_ops = [], []
        for op in ops:
            if hasattr(op, "_is_Attribute"):
                a_ops.append(op)
            elif hasattr(op, "_is_Relation"):
                r_ops.append(op)
            else:
                #op is not Attribute or Relation, raise TypeError
                raise TypeError(
                "all optional positional arguments must be of type "
                "Attribute or Relation")

        #Sort provided ops so that attributes are added first
        sorted_a_ops = sorted(a_ops, key=lambda x: x._label)
        sorted_r_ops = sorted(r_ops, key=lambda x: x._subscript)

        sorted_ops = sorted_a_ops + sorted_r_ops

        #for each optional positional argument op
        for op in sorted_ops:
            #if op is an Attribute
            if hasattr(op, "_is_Attribute"):
                #if attribute is not a duplicate add attribute to objects list
                #of attributes                                               
                if op not in self._attributes:
                    self._attributes.append(op)
                    continue

            #if op is a Relation
            elif hasattr(op, "_is_Relation"):

                #prevent duplicate subscripts
                if op._subscript in self._relations.keys():
                    raise ValueError(
                        "Duplicate subscripts not permitted in "
                        "AttributeStructure.")

                #if D(R) is within cartesian product of attribute labels
                if set(op.get_DR()) <= set(self.get_labels()):
                    #add op to object's relation dict
                    self._relations[op._subscript] = op
                    #start at top of loop to not raise exception
                    continue
                #op's D(R) is invalid, raise ValueError
                else:
                    raise ValueError(
                        "D(R) must be a subset of cartesian product "
                        "of some combination of attributes")

    def __eq__(self, other):
        """
        Return a boolean for whether self and other 
        AttributeStructure objects are equal.
        """

        #Attribute sets different length, not equal
        if len(self._attributes) != len(other._attributes):
            return False
        else:
            for i in range(len(self._attributes)):
                #Attributes not equal
                if self._attributes[i] != other._attributes[i]: 
                    return False            
        
        s_keys, o_keys = self._relations.keys(), other._relations.keys()
        #Different amount of relations, not equal 
        if len(s_keys) != len(o_keys): 
            return False                                 
        for s_key in s_keys:
            for o_key in o_keys:
                if self._relations[s_key] == other._relations[o_key]: 
                    break
            #No match for a relation found, not equal
            else: 
                return False
        #Relations and Attributes are equal, structures are equal
        return True
    
    def __ne__(self, other):
        """Determine if two AttributeStructure's are not equal."""
        return not self.__eq__(other)

    def __add__(self, other):
        """
        Implement + to add Attribute's, Relation's, or AttributeStructure's
        easily.
        """
        
        new_astr = deepcopy(self)

        #handle adding Attribute's to this AttributeStructure
        if hasattr(other, "_is_Attribute"):
            #Add other Attribute if it's label isn't in this AttributeStructure
            if other._label not in self.get_labels():
                new_astr._attributes.append(deepcopy(other))
        
        #handle adding Relation's to this AttributeStructure
        elif hasattr(other, "_is_Relation"):
            #if other Relation has a duplicate subscript raise ValueError
            if other._subscript in self._relations.keys():
                raise ValueError(
                    "Duplicate subscripts not permitted.")

            #check if other Relation's D(R) is a subset of this 
            #AttributeStructure's Attribute labels
            if set(other._DR) <= set(self.get_labels()): 
                new_astr._relations[other._subscript] = deepcopy(other)
            else: 
                raise ValueError(
                    "operand must have all members of D(R) in this "
                    "AttributeStructure's attribute labels.")
        
        #handle adding AttributeStructure to this AttributeStructure
        elif hasattr(other, "_is_AttributeStructure"):
            for attribute in other._attributes:
                new_astr += deepcopy(attribute)
            for relation in other._relations.values():
                new_astr += deepcopy(relation) 
        
        else:
            raise TypeError(
                "Only Relation or Attribute objects can be added to an " 
                "AttributeStructure.")

        return new_astr

    def __sub__(self, other):
        """
        Implement - to remove Attribute's or Relation's easily (including the
        set of Attribute's and Relation's from an AttributeStructure).
        """

        #Handle removal of Attribute
        if hasattr(other, "_is_Attribute"):
            for i, attribute in enumerate(self._attributes):
                if attribute._label == other._label:
                    del self._attributes[i]
                    break
            else: 
                raise ValueError("No attribute with label " + str(label))
        
        #Handle removal of Relation
        elif hasattr(other, "_is_Relation"):
            if not subscript in self._relations.keys(): 
                raise KeyError("No relation with subscript " + str(subscript))
            else:
                self._relations.pop(subscript, None)
        
        #handle adding AttributeStructure to this AttributeStructure
        elif hasattr(other, "_is_AttributeStructure"):
            for attribute in other._attributes:
                self -= attribute
            for relation in other._relations.values():
                self -= relation 
        
        else:
            raise TypeError(
                "Only Relation or Attribute objects can be removed to an " 
                "AttributeStructure.")

        return self

    def __iadd__(self, other):
        """
        Implement += to add Attribute's, Relation's, or AttributeStructure's
        easily.
        """

        return self.__add__(other)

    def __isub__(self, other):
        """
        Implement -= to remove Attribute's or Relation's easily (including the
        set of Attribute's and Relation's from an AttributeStructure).
        """

        return self.__sub__(other)

    def __deepcopy__(self, memo):
        """Return a deep copy of this AttributeStructure object."""

        import copy

        attributes_copy = copy.deepcopy(self._attributes)
        relations_copy = copy.deepcopy(self._relations).values()

        ops_copy = [attribute for attribute in attributes_copy] + [relation for relation in relations_copy]

        return AttributeStructure(*ops_copy)
    
    def set_attributes(self, attributes):
        """
        Set attributes to list of attributes. 
        
        raise TypeError if a is not a list of attributes.
        """
        
        if not isinstance(attributes, list):
            raise TypeError('a must be a list')
        else:
            for attr in attributes:
                if not hasattr(attr, "_is_Attribute"):
                    raise TypeError('each entry of a must be an attribute')
            self._attributes = attributes
    
    def set_relations(self, relations): 
        """
        Set relations to dictionary of subscript:Relation pairs.

        raise TypeError if a is not a list of attributes.
        """
        
        if not isinstance(relations, dict):
            raise TypeError('r must be a dictionary')
        else:
            for s, R in relations:
                if not isinstance(s, int) or not hasattr(R, "_is_Relation"):
                    raise TypeError(
                        "dictionary must be of form subscript:Relation")
            self._relations = relations

    def get_labels(self):
        """Return labels of Attributes within this AttributeStructure."""
        return [a._label for a in self._attributes]

    def get_attribute(self, label):
        """Get attribute by label; returns None if not found in attributes."""
        for attr in self._attributes:
            if attr._label == label:
                return attr
        return None
    
    def get_relation(self, subscript): 
        """get relation by subscript; returns None if not found in relations."""
        if subscript in self._relations: 
            return self._relations[subscript]
        else: 
            raise KeyError("No relation with subscript " + str(subscript))

    def get_subscripts(self): 
        """Return this AttributeStructure's Relation subscripts."""
        return self._relations.keys()

    def get_cardinality(self):
        """Return cardinality of this AttributeStructure."""
        return len(self._attributes)

    def __str__(self):
        """Human-readable representation of this AttributeStructure."""
        #Build sorted list of subscripts each separated by a comma
        r_string = ''.join(['R' + str(i) + ',' for i in sorted([i for i in self._relations.keys()])])[:-1] + ')'
        #Add attributes string (e.g. size: {(0,...,651)}, objs: {True,False}, )
        return '(' + ''.join([str(attr) + ', ' for attr in self._attributes])[:-2] + ' ; ' + r_string

    def __repr__(self):
        """Machine representation of this AttributeStructure."""
        self._relations[1] = None
        self._relations[3] = None
        r_string = ",".join(['R' + str(i) for i in sorted(self._relations.keys())])
        a_str = ",".join(sorted([str(attr) for attr in self._attributes]))
        return r_string + ";" + a_str

def main():
    """Main method; quick testing."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"])

    astr = AttributeStructure(a)
    #astr += b
    #astr -= a
    #print astr + c


if __name__ == "__main__":
    main()