"""Attribute Structure class."""

from Attribute import Attribute
from Relation import Relation

class AttributeStructure(object):
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

        #for each optional positional argument op
        for op in ops:
            #if op is an Attribute
            if isinstance(op, Attribute):
                #if attribute is not a duplicate                                               
                if op not in self._attributes:
                    self._attributes.append(op)#add attribute to objects list of attributes
                    continue#start at top of loop to not raise exception

            #if op is a Relation
            if isinstance(op, Relation):
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

            #op is not Attribute or Relation, raise TypeError
            raise TypeError(
                "all optional positional arguments must be of type "
                "Attribute or Relation")

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
        #Attribute sets different length, not equal
        if len(self._attributes) != len(other._attributes): return True
        else:
            for i in range(len(self._attributes)):
                #Attributes not equal
                if self._attributes[i] != other._attributes[i]: return True
        
        s_keys, o_keys = self._relations.keys(), other._relations.keys()
        #Different amount of relations, not equal 
        if len(s_keys) != len(o_keys): return True
        for s_key in s_keys:
            for o_key in o_keys:
                if self._relations[s_key] == other._relations[o_key]: break
            #No match for a relation found, not equal
            else: return True

        #Relations and Attributes are equal, structures are equal
        return False

    def deep_copy(self):
        """Return a deep copy of this AttributeStructure object."""

        import copy

        attributes_copy = copy.deepcopy(self._attributes)
        relations_copy = copy.deepcopy(self._relations).values()

        ops_copy = [attribute for attribute in attributes_copy] + [relation for relation in relations_copy]

        return AttributeStructure(*ops_copy)

    def get_attributes(self): return self._attributes
    
    def set_attributes(self, a): 
        'Set attributes to list of attributes; raise TypeError if a is not a list of attributes'
        if not isinstance(a, list): raise TypeError('a must be a list')             #Arguement passed must be a list
        else:   
            for attr in a:
                if not isinstance(attr, Attribute):                                     #Raise TypeError if any member of a is not an attribute
                    raise TypeError('each entry of a must be an attribute')
            self._attributes = a

    def get_relations(self): return self._relations
    
    def set_relations(self, r): 
        'Set relations to dictionary of int(subscript):Relation pairs; raise TypeError if a is not a list of attributes'
        if not isinstance(r, dict): raise TypeError('r must be a dictionary')           #Raise TypeError if arguement passed is a not dictionary
        else:
            for k, v in r:
                if not isinstance(k, int) or not isinstance(v, Relation):               #Raise TypeError if members of r are not int:Relation
                    raise TypeError(
                        'dictionary must be of form ' + 
                        'int(i.e., subscript):Relation'
                        )
            self._relations = r

    def add_attribute(self, a):
        'Add attribute to attribute structure; returns 0 on success, 1 on failure, raise TypeError when a is not an Attribute'
        if not isinstance(a, Attribute): 
            raise TypeError('a must be of type Attribute')                              #If arguement is actually an instance of Attribute
        else:
            if a._label not in self.get_labels():                                       #Check if a is already in attribute structure
                self._attributes.append(a)
                return 0
        return 1
    
    def add_relation(self, r): 
        'Add relation to relations; raise TypeError when r is not a Relation'
        if not isinstance(r, Relation): 
            raise TypeError('r must be of type Relation')                               #If arguement is actually an instace of Relation
        else: 
            if set(r.get_DR()) <= set(self.get_labels()): 
                self._relations[r.subscript] = r                                        #check if D_of_R memebers are in attribute labels
            else: raise ValueError(
                "r must have all members of D_of_R in attribute labels"
                )

    def get_labels(self): return [a.get_label() for a in self._attributes]

    def get_attribute(self, label):
        'get attribute by label; returns None if not found in attributes'
        for attr in self._attributes:
            if attr._label == label: return attr
        return None
    
    def get_relation(self, subscript): 
        'get relation by subscript; returns None if not found in relations'
        if subscript in self._relations: return self._relations[subscript]
        else: raise KeyError("No relation with subscript " + str(subscript))
    
    def remove_attribute(self, label):
        'remove attribute with label; raise KeyError if label doesnt exist'
        for i in range(len(self._attributes)):
            if self._attributes[i]._label == label: 
                del self._attributes[i]
                break                                                                   #Get index for removal
        else: raise KeyError("No attribute with label " + str(label))
    
    def remove_relation(self, subscript):
        if not subscript in self._relations.keys(): 
            raise KeyError("No relation with subscript " + str(subscript))
        else: 
            del self._relations[subscript]                                              #delete relation with subscript in AttributeStructure
            for i in Relation.subscripts:
                if i == subscript: del Relation.subscripts[i]                           #delete subscript in Relation.subscripts

    def get_subscripts(self): return self._relations.keys()

    def get_cardinality(self): return len(self._attributes)                         #Get cardinality of Attribute Structure

    def __str__(self):
        r_string = ''.join(
                ['R' + str(i) + ',' for i in sorted(                                    #list comprehension to build a sorted list of subscripts each separated by a comma
                    [i for i in self._relations.keys()]
                    )
                ]
            )[:-1] + ')'                                                                #drop trailing comma and add closing parenthesis
        return '(' + ''.join(
            [str(attr) + ', ' for attr in self._attributes]                             #list comprehension to build attributes string (e.g. size: {(0,...,651)}, objs: {True,False}, )
            )\
            [:-2] + ' ; ' + r_string                                                    #drop trailing ", " and add ; + relation string build above

def main():
    """Main method; quick testing."""

    a, b, c = Attribute("a", []), Attribute("b", []), Attribute("c", [])
    r = Relation("R1(a,b) <=> ", ["a", "b"])

    a = AttributeStructure(a, b, c, r)

if __name__ == "__main__":
    main()