"""."""

from copy import deepcopy
from functools import total_ordering
from Attribute import Attribute

@total_ordering
class ValueSet(object):
    """."""

    _base_types = [int, float, long, str]
    _object_types = []

    @classmethod
    def add_object_type(cls, object_identifier):
        """Add compatibility for object."""
        #Ensure object identifiers are strings
        if not isinstance(object_identifier,str):
            raise TypeError("Object identifier's must be strings")
        import re
        
        #Ensure they have the correct form
        if not re.match("_is_[A-Za-z]", object_identifier):
            raise ValueError(
                "object identifier must be of form _is_[object name]")
        
        #Add id to list of id's if it's not a duplicate
        if object_identifier not in cls._object_types:
            cls._object_types.append(object_identifier)

    def __init__(self, valueset):
        """Construct a ValueSet object."""
        #Save parsed output
        self._values = ValueSet._parse(valueset)
        self._is_ValueSet = True

    def __eq__(self, other):
        """Implement == for ValueSet object."""
        pass

    def __le__(self, other):
        """Implement <= for ValueSet object."""
        pass

    def __ne__(self, other):
        """Implement != for ValueSet object."""
        pass

    def __iter__(self):
        """Implement iterator for ValueSet."""
        for value in self._values:
            yield value

    def __deepcopy__(self, memo):
        """."""
        pass

    @staticmethod
    def _parse(values):
        """Parse a list into standard format."""
        def _split_by_types(values):
            """Split valueset by types of elements within it."""
            #initialize a dictionary to separate types
            from collections import defaultdict
            type_lists = defaultdict(list)

            #for each value provided
            for value in values:
                #if it's a base type, simply add to it's corresponding list.
                if type(value) in ValueSet._base_types:
                    if value not in type_lists[type(value)]:
                        type_lists[type(value)].append(value)
                    continue
                
                #if it's an object type, check to see if it is in supported
                #object types
                identifier = None
                for object_identifier in ValueSet._object_types:
                    if hasattr(value, object_identifier):
                        #Ensure no object has 2 identifiers
                        if identifier:
                            raise AttributeError(
                                "Any object passed must have only 1 "
                                "supported identifier")
                        identifier = object_identifier

                #store object in its corresponding list if it's not a duplicate
                if identifier:
                    if value not in type_lists[identifier]:
                        type_lists[identifier].append(value)
                else:
                    raise TypeError(
                        str(type(value)) + " not supported")

            return type_lists

        #only accept sets and lists for valueset parameter
        if not isinstance(values, list) and not isinstance(values, set):
            raise TypeError("values paramter must be a list or set")

        #make copy of input before processing
        input_set = deepcopy(values)

        #convert set to list
        if isinstance(input_set, set):
            input_set = list(input_set)

        type_lists = _split_by_types(values)

        for k,v in type_lists.iteritems():
            print str(k) + ": \t" + str(v)

        output_set = []
        return output_set











def parse(set1):
    """
    Parse set1 paramter into a list of individual elements and low-high tuples

    parse considers the following types of individual element in the set1 paramter (of type list):
    individual elements,                                                            e.g. 'f', 1, 'word', 100, 12.34             ->      ['f', 1, 'word', 100, 12.34]
    a group of elements in set notation,                                            e.g. '{1, 2, 3, 7, 9, 'f', 12.34}'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a group of elements in a tuple,                                                 e.g. '(1, 2, 3, 7, 9, 'f', 12.34)'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a group of elements in brackets,                                                e.g. '[1, 2, 3, 7, 9, 'f', 12.34]'          ->      [1, 2, 3, 7, 9, 'f', 12.34]
    a string (note: commas in stirng are ignored; a string is a string),            e.g. 'fresh,yo'                             ->      ['fresh,yo']
    continuous ranges denoted by ellipses (note: this creates a low-high tuple),    e.g. '-12.3,...,10' or '15,...,90,...,2000' ->      [(-12.3, 10.0), (1, 2000)]
    boolean types,                                                                  e.g. True, False                            ->      [True, False]
    iterables (note: iterables are groups, however low-highs are auto parsed),      e.g. (1,2,3), [4,5,6], (1,90), (10,'f')     ->      [[1,2,3], [4,5,6], (1,90), [10, 'f']]

    parse supports arbitrarily nested groups e.g. '{-11111,0,{12,3,{23,{69,{80,7,900}}},5},651,900}', however, don't mix and match different grouping characters in same string
    (note: nested groups allow for duplicates, that is, you can have copies of the same nested group or multiple single elements on the same level provided they parse to the same output)

    Overlapping low-high tuples are collapsed and individual numbers are absorbed by low-high tuples when they fall within range.
    low-high tuples where low==high are converted to a single number
    if low or high is a float, by default the other will be converted to a float

    note: when flattening, if flattened list has a float with the same value as an int also in list, 
    whichever one comes 2nd is treated as a duplicate and deleted as flatten() casts list to built in python type set and back

    as of now, parse is used in the functions: 
    Attribute.set_possible_values(), 
    is_alternate_extension(),
    is_subset(),
    get_set_theoretic_difference(),
    State.set_ascription()

    input:
    set1: a list containing any combination of above types
    flat: a boolean to determine whether or not to flatten any nested groups
    
    exceptions will be raised in the following cases:
    set1 paramter is not a list,
    a grouping is invalidly formatted i.e., it is not a group of correctly formatted elements separated by single commas 
    starting with a single opening character and ending with that character's corresponding closing character
    (note:inner quotes are not supported as of now; grouping elements will try to be parsed to ints or floats and default to string if parsing fails),
    ellipses begin or end a potential low-high tuple string (note: this is for time being until infinite sets are figured out),
    a grouping that contains a subgroup with different grouping characters than the supergroup

    output:
    a list containing only single elements and low-high tuples.
    """

    #print get_caller()

    #handle exception case 1
    if not isinstance (set1, list):                                                 #if parse parameter is not of type list
        raise TypeError(                                                                #explicitly raise a TypeError
            'set1 parameter must be of type list'
            )

    def parse_element(e):
        """parse an individual element according to specifications laid out in parse docstring"""

        def is_iterable(iter_element):
            """Return boolean for whether or not iter_element parameter is an iterable"""
            
            if isinstance(iter_element, tuple):                                     #if iter_element parameter is a tuple
                if len(iter_element) == 2:
                    left_valid = type(iter_element[0]) == int or type(iter_element[0]) == float
                    right_valid = type(iter_element[1]) == int or type(iter_element[1]) == float 
                    if left_valid and right_valid:
                        return False
                return True                                                             #return True
            elif isinstance(iter_element, list):                                        #if iter_element parameter is a list
                return True                                                             #return True
            elif isinstance(iter_element, dict):                                        #if iter_element parameter is a dict
                raise TypeError(                                                        #raise TypeError; dicts not supported as elements
                    'elements of type dict are not supported'
                    )
            else:
                return False

        def iterable_to_grouping(iter_element):
            """Return list of iterable iter_element parameter"""

            if isinstance(iter_element, tuple):                                     #if iter_element parameter is a tuple
                return list(iter_element)                                               #return it as a list
            elif isinstance(iter_element, list):                                        #if iter_element parameter is a list
                return iter_element                                                     #return it as it is

        def is_low_high_tuple(tup):
            if isinstance(tup, tuple):                                          #if tup parameter is a tuple
                if len(tup) == 2:
                    left_valid = type(tup[0]) == int or type(tup[0]) == float
                    right_valid = type(tup[1]) == int or type(tup[1]) == float 
                    if left_valid and right_valid:
                        return True
            return False

        def enforce_low_high_tuple(tup):
            """Given a low-high tuple candidate, return it in correct order or as single"""

            float_flag = type(tup[0]) == float or type(tup[1]) == float                 #determine if either low or high is a float

            if tup[0] == tup[1]:                                                        #if low equals high
                if float_flag:                                                          #return single as a float if either low or high is a float
                    return float(tup[0])                                                #return as a single
                else:                                                                   
                    return tup[0]                                                       #simply return single
            if tup[0] < tup[1]:                                                     #if low is less than high
                if float_flag:                                                          #if either low or high is a float
                    return (float(tup[0]), float(tup[1]))                               #return as a single
                else:                                                                   #otherwise
                    return e                                                            #simply return
            if tup[0] > tup[1]:                                                     #if low is greater than high
                if float_flag:                                                          #if either low or high is a float
                    return (float(tup[1]), float(tup[0]))                               #return as floats in reversed order
                else:                                                                   #otherwise
                    return (tup[1], tup[0])                                             #return in reverse

        #handles exception cases 2, 4
        def is_grouping(s):
            """Return boolean for whether or not s parameter is a grouping."""
            
            def do_left_right_match(l, r):
                """Return boolean for whether left and right grouping chars match."""
                
                if l == '{':
                    if r == '}':
                        return True
                    else:
                        return False
                if l == '(':
                    if r == ')':
                        return True
                    else:
                        return False
                if l == '[':
                    if r == ']':
                        return True
                    else:
                        return False

            def is_inside_correctly_formatted(left, right, grouping):
                """Return boolean for whether or not grouping is formatted correctly inside of grouping characters."""

                def contains_other_grouping_chars(left, right, grouping_string):
                    """Return boolean for whether or not grouping_string parameter contains subgroup with different grouping characters than supergroup"""
                    
                    if left == '{' and right == '}':                                    #if left and right grouping chars in uspergroup are {}
                        if '(' in grouping_string or ')' in grouping_string\
                         or '[' in grouping_string or ']' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    elif left == '(' and right == ')':                                  #if left and right grouping chars in uspergroup are ()
                        if '{' in grouping_string or '}' in grouping_string\
                         or '[' in grouping_string or ']' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    elif left == '[' and right == ']':                                  #if left and right grouping chars in uspergroup are []
                        if '{' in grouping_string or '}' in grouping_string\
                         or '(' in grouping_string or ')' in grouping_string:           #if other grouping characters are in string, return True
                            return True
                        else:                                                           #otherwise, return True
                            return False
                    else:                                                               #left and right are mismatched, explicitly raise ValueError
                        raise ValueError(
                            'cannot have mismatched grouping ' +
                            'characters at begin and end of a grouping'
                            )

                group_elements = grouping.split(',')                                    #split grouping up by commas

                if '' in group_elements:                                                #if two commas are used in a row, incorrect formatting
                    return False                                                        #return False
                else:                                                                   #elements are separated by single commas, correct formatting
                    if not contains_other_grouping_chars(left, right, grouping):        #if subgroup in grouping does not have different grouping chars
                        return True                                                     #return True
                    else:                                                               #otheriwse return False
                        return False

            if not isinstance(s, str):                                              #a grouping has to be of type string
                return False
            
            left = s[0]                                                                 #get first character of string
            right = s[-1]                                                               #get last character of string

            left_cond = left == '{' or left == '(' or left == '['                       #check if first char is a left grouping char
            right_cond = right == '}' or right == ')' or right == ']'                   #check if last char is a right grouping char
            
            if left_cond and right_cond:                                                #if both first and last chars are grouping chars
                match = do_left_right_match(left, right)                                #check if they match
                if match == True:                                                       #if they do, return True
                    format_flag = is_inside_correctly_formatted(                        #determine if inside is correctly formatted
                        left,
                        right,
                        s[1:len(s)-1]
                        )
                    if format_flag:                                                 #if inside of grouping is correctly formatted
                        return True                                                     #return True
                    else:                                                               #inside of grouping is incorrectly formatted
                        raise ValueError(                                               #raise ValueError
                            'inside of grouping is incorrectly formatted'
                            )
                else:                                                                   #they don't match but grouping chars are used
                    raise ValueError(                                                   #raise ValueError
                        'cannot have a grouping with mismatched ' +
                        'grouping characters in element of input_list'
                        )
            
            return False                                                                #not a grouping if first and last chars aren't grouping chars, return False

        def parse_grouping(group_string):
            """Return a parsed grouping element as an int, float, or string."""

            def extract_subgroup(left, right, expr):
                """
                Return boolean for whether or not expr parameter is balanced, that is, whether opening and closing characters have same count.
                
                input:
                left: left grouping character
                right: right grouping character
                expr: expression to extract subgroups from

                output:
                a list of subgroups present in expr parameter
                """

                s = Stack()
                balanced = True
                index = 0

                subgroups = []
                build_str = ''

                while index < len(expr) and balanced:                                   #while index is less than length of expr and expr is balanced
                    symbol = expr[index]                                                #get char at index of expr
                    
                    if symbol != left and symbol != right:                          #if the symbol is neither opening or closing grouping char
                        build_str += symbol                                             #add it to the build string
                        index = index + 1                                               #increment index
                        continue                                                        #loop to next char

                    if symbol == left:                                                  #if symbol is opening grouping char
                        s.push(symbol)                                                  #push it into the stack
                        build_str += symbol                                             #also add it to build string
                    else:                                                               #not opening goruping char
                        if s.isEmpty():                                                 #if stack is empty
                            balanced = False                                            #expr is not balanced
                        else:                                                           #otherwise
                            build_str += right                                          #add closing grouping char to build string
                            s.pop()                                                     #pop opening character off of stack

                    if s.isEmpty():                                                     #if stack is empty at this point in expr, we may have a built subgroup
                        subg_index = build_str.find(left)                               #get starting index of subgroup
                        if subg_index != -1:                                            #if a subgroup is indeed present
                            subgroups.append(                                           #extract it and add to subgroups list
                                build_str[subg_index: len(build_str)]
                                )
                        build_str = ''                                                  #reset build string
                    index = index + 1                                                   #and increment index

                if balanced and s.isEmpty():                                            #if the expression is thus far balanced and the stack has been depleted, it is totally balanced
                    return subgroups                                                    #return the subgroups
                else:                                                                   #not a balanced expression, raise ValueError
                    raise ValueError(
                        'all grouping expressions must be balanced'
                        )

            grouping_left = group_string[0]                                             #get left grouping character
            grouping_right = group_string[len(group_string)-1]                          #get right grouping character
            trimmed_group_string = group_string[1:len(group_string)-1]                  #trim the group chars off of the string

            subgroups = extract_subgroup(                                               #extract subgroups from group_string
            grouping_left, 
            grouping_right, 
            trimmed_group_string
            ) 

            for subgroup in subgroups:                                                  #for every subgroup extracted from group_string
                temp_string = trimmed_group_string                                      #store temportary copy of trimmed string
                trimmed_group_string = trimmed_group_string.replace(                    #replace trimmed string with itself minus the subgroup
                    subgroup + ',',
                    ''
                    )
                if temp_string == trimmed_group_string:                                 #subgroup was adjacent to end of trimmed string and thus had no comma
                    trimmed_group_string = trimmed_group_string.replace(                #replace it with itself without subgroup and remove trailing comma for groupings split
                        subgroup,
                        '')[:-1]

            grouping_output = []                                                        #create list to store parsed elements of grouping

            for subgroup in subgroups:
                grouping_output.append(parse_grouping(subgroup))

            grouping = trimmed_group_string.split(',')                                  #split grouping string into constituent elements
            
            if '' in grouping:                                                          #if empty strings have been incurred after trimming (during nested singletons)
                grouping.remove('')                                                     #remove them

            for ge in grouping:                                                     #for each element of the grouping
                parsed_ge = parse_int_float_string(ge)                                  #parse element to int, float, or string
                grouping_output.append(parsed_ge)                                       #append parsed element to grouping output list      

            return grouping_output                                                      #return list containing all parsed elements

        #handles exception case 3
        def can_convert_to_low_high_tuple(s):
            """Return boolean for whether or not s parameter can be converted to low-high tuple"""

            def is_convertable(string):
                """Return boolean for whether or not string parameter contains an ellipsis"""

                def valid_numerics_and_ellipses(vne_string):
                    """Return whether or not vne_string parameter contains only numeric characters, commas, and ellipses in appropriate places"""

                    e_elements = vne_string.split(',')

                    start_ellipses = e_elements[0] == '...'                             #store if ellipses begin potential low-high tuple string
                    end_ellipses = e_elements[len(e_elements) - 1] == '...'             #store if ellipses begin potential low-high tuple string

                    if start_ellipses or end_ellipses:                              #if ellipses begin or end a low-high tuple string
                        raise ValueError(                                               #raise ValueError
                            'infinite sets not supported; ' + 
                            'ellipses cannot begin or end ' +
                            'a low-high tuple string'
                            )
                    for e_element in e_elements :                                       #for each element in e_elements
                        parsed_e_element = parse_int_float_string(e_element)            #parse e_element to int, float, or string
                        
                        is_int = type(parsed_e_element) == int                          #store condition for if parsed_e_element is an int
                        is_float = type(parsed_e_element) == float                      #store condition for if parsed_e_element is an float

                        if not is_int and not is_float:                             #if parsed_e_element is not an int or float
                            if parsed_e_element != '...':                               #parsed_e_element is a string; if it's not an ellipsis
                                return False                                            #return False

                    return True                                                         #elements all check out, return True

                if isinstance(string, str):                                         #if string parameter is a string
                    if '...' in string:                                             #if string contains an ellipsis
                        
                        format_flag = valid_numerics_and_ellipses(string)               #determine if string parameter contains
                        if format_flag:                                             #if string contains only numerics and ellipses all separated by commas
                            return True                                                 #return True
                        else:                                                           #otherwise, return False
                            return False
                    else:                                                               #string does not contain ellipsis
                        return False                                                    #return False

                #Note: returns None here which evaluates to False

            if is_convertable(s):                                                       #if s paramter is convertable to low-high tuple
                return True                                                             #return True
            else:                                                                       #s parameter is not convertable to low-high tuple
                return False                                                            #return False

        def convert_to_low_high_tuple(lh_string):
            """Return a low-high tuple converted from lh_string parameter"""

            lh_elements = lh_string.split(',')                                          #split lh_string into constituent elements
            
            ellipses_indicies = []
            for i in reversed(range(len(lh_elements))):                             #get indicies of ellipses greatest first
                if lh_elements[i] == '...':
                    ellipses_indicies.append(i)                                         #append index if it corresponds to an ellipses

            for i in ellipses_indicies:                                             #for each index corresponding to an ellipses
                del lh_elements[i]                                                      #delete ellipses element
            
            low = min(lh_elements)                                                      #get the smallest element for low-high tuple
            high = max(lh_elements)                                                     #get the highest element for low-high tuple


            float_flag = False
            if '.' in low or '.' in high:                                               #if low or high are a float, set float flag
                float_flag = True


            if float_flag:                                                              #if low or high is a float, cast both to float
                if float(low) == float(high):                                           #if low == high, return single number
                    return float(low)
                else:
                    if float(low) < float(high):                                        #this condition is for when both are negative
                        return (float(low), float(high))                                #return low-high float tuple
                    else:
                        return (float(high), float(low))                                #return low-high float tuple
            else:                                                                       #otherwise, cast both to ints
                if int(low) == int(high):                                               #if low == high, return single number
                    return int(low)
                else:
                    if int(low) < int(high):                                            #this condition is for when both are negative
                        return (int(low), int(high))                                    #return low-high int tuple
                    else:
                        return (int(high), int(low))                                    #return low-high int tuple

        iter_flag = is_iterable(e)                                                      #determine if element is an iterable

        if iter_flag:                                                                   #if element is an iterable
            return iterable_to_grouping(e)                                              #return it as a grouping

        tuple_flag = is_low_high_tuple(e)

        if tuple_flag:                                                                  #if it is potentially a low-high tuple
            return enforce_low_high_tuple(e)                                            #return it with correct formatting

        grouping_flag = is_grouping(e)                                                  #determine if element is a grouping
        
        if grouping_flag:                                                               #if element is a grouping
            return parse_grouping(e)                                                    #get the parsed group
        
        low_high_flag = can_convert_to_low_high_tuple(e)                                #determine if element can be converted to low-high tuple

        if low_high_flag:                                                               #if element is convertable to a low-high tuple 
            return convert_to_low_high_tuple(e)                                         #return low-high tuple conversion

        return e                                                                        #e is a single element, return it simply

    def separate_tuples(elements):
        """Return a list of tuples and a list of non-tuples from elements parameter."""

        tuples = []                                                                     #create a list for tuples
        non_tuples = []                                                                 #create a list for non-tuples

        for element in elements:                                                        #for each element in elements
            if isinstance(element, tuple):                                              #if that element is a tuple
                tuples.append(element)                                                  #append it to tuples list
            else:                                                                       #otherwise, append to non-tuples list
                non_tuples.append(element)

        return tuples, non_tuples                                                       #return the two lists

    def floatify(tuples):
        """Return low-high tuples without mismatched types; modifies tuples parameter in place."""

        for i, tup in enumerate(tuples):                                                #for each low-high tuple
            low_type = type(tup[0])                                                     #get type of low
            high_type = type(tup[1])                                                    #get type of high

            if low_type == float or high_type == float:                                 #if either low or high is a float
                tuples[i] = (float(tup[0]), float(tup[1]))                              #replace tup with copy where both low and high are floats

    def flatten(non_tuples):
        """Return a flattened non_tuples."""

        def flatten_list(lis):
            """Given a list, possibly nested to any level, return it flattened."""
            
            new_lis = []                                                                #create new list
            for item in lis:                                                            #for item in nth list
                if type(item) == type([]):                                              #if type of item is a list therefore possible to recur on
                    new_lis.extend(flatten_list(item))                                  #extend new list with the (n+1)th list
                else:                                                                   #not a list
                    new_lis.append(item)                                                #just add to new list
            return new_lis                                                              #return nth list

        list_non_tuples = []                                                            #creat list of lists, i.e., groupings in non_tuples
        single_non_tuples = []                                                          #create list of singles
        
        for non_tuple in non_tuples:                                                    #for every non-tuple
            if type(non_tuple) == list:                                                 #if its a list, add to list non-tuples
                list_non_tuples.append(non_tuple)
            else:                                                                       #not a list, has to be a single
                single_non_tuples.append(non_tuple)                                     #add to single non-tuples

        flat_non_tuples = list(                                                         #flatten the list non-tuples and remove duplicates
            set(flatten_list(list_non_tuples)))                       

        return flat_non_tuples + single_non_tuples                                      #join the singles with the flattened list elements

    def merge_singles(element):
        """
        function to merge single integers with tuples that either contain it or are 1 off on either the low or high
        e.g. if tuple x = (10, 50), and integer y = 9, 10-50, or 51, it will be merged
        """

        for i, x in enumerate(element):
            for j, y in enumerate(element):
                if isinstance(x, tuple) and isinstance(y, int):                         #dont have to check if i != j, if i == j cant be of differnet types
                    if x[0] <= y <= x[1]:                                               #if a single int is contained in a high-low tuple, remove it
                        del element[j]
                        return True
                    
                    if y == x[0] - 1:                                                   #if a single int equals 1 lower than a tuples low, combine them and delete old tuple and single
                        element.append((y, x[1]))
                        if i < j:
                            del element[j]
                            del element[i]
                        if j < i:
                            del element[i]
                            del element[j]
                        return True
                    
                    if y == x[1] + 1:                                                   #if a single int equals 1 higher than a tuples high, combine them and delete old tuple and single
                        element.append((x[0], y))
                        if i < j:
                            del element[j]
                            del element[i]
                        if j < i:
                            del element[i]
                            del element[j]
                        return True
                elif isinstance(x, tuple) and isinstance(y, float):                     #dont have to check if i != j, if i == j cant be of differnet types
                    
                    global float_df                                                     #bring float differential float_df into local namespace 

                    if x[0] - float_df <= y <= x[1] + float_df:                         #if a single int is contained in a high-low tuple, remove it
                        del element[j]
                        return True
                        
        return False

    def delete_duplicate_subgroups(subgroups):
        """Return boolean for whether or not a duplicate subgroup was successfully deleted from subgroups parameter"""

        for i, nt1 in enumerate(subgroups):
            for j, nt2 in enumerate(subgroups):
                if i != j:                                                              #if indicies aren't the same
                    if type(nt1) == type(nt2) and type(nt1) == list:                    #if both nt1 and nt2 are sublists
                        if nested_equivalence(nt1, nt2):                     #if they are deeply equivalent without shrinking
                            del subgroups[i]
                            return True
        return False

    input_list = copy.copy(set1)                                                        #create copy of input to avoid pass by reference
    output_list = []                                                                    #create empty output list

    for element in set1:                                                                #for each element in input_list
        parsed_element = parse_element(element)                                         #get its parsed equivalent
        output_list.append(parsed_element)                                              #and store it in output list

    tuples, non_tuples = separate_tuples(output_list)                                   #split low-high tuples from not low-high tuples

    while collapse(tuples): pass                                                        #collapse overlapping tuples

    floatify(tuples)                                                                    #take care of mismatched in/float low-high tuples

    global flat_flag                                                                    #bring global flat_flag into local namespace

    if flat_flag:                                                                       #if flat parameter is turned on
        non_tuples = flatten(non_tuples)                                                #flatten non-tuples
    else:                                                                               #flat parameter is off
        while delete_duplicate_subgroups(non_tuples): pass

    output_list = tuples + non_tuples                                                   #combine tuples and non-tuples back together

    while merge_singles(output_list): pass                                          #merge singles into low-high tuples

    return output_list                                                                  #send back parsed list

def main():
    """."""
    ValueSet.add_object_type("_is_Attribute")
    v = ValueSet([1, 1.0, 1L, '', Attribute("label", [])])

if __name__ == "__main__":
    main()