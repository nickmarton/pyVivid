.. vivid documentation master file, created by
   sphinx-quickstart on Sun Jan 17 01:43:43 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vivid's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

.. automodule:: assignment
 
.. autoclass:: Assignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__

.. automodule:: assumption_base
 
.. autoclass:: AssumptionBase
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __iadd__, __str__, __repr__, __len__, __getitem__, __iter__, __contains__, __deepcopy__

.. automodule:: attribute
 
.. autoclass:: Attribute
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __deepcopy__, __str__, __repr__, __hash__

.. automodule:: attribute_interpretation
 
.. autoclass:: AttributeInterpretation
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __iter__, __str__, __repr__

.. automodule:: attribute_structure
 
.. autoclass:: AttributeStructure
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __add__, __sub__, __iadd__, __isub__, __getitem__, __contains__, __deepcopy__, get_labels, get_subscripts, get_cardinality, __str__, __repr__

.. automodule:: attribute_system
 
.. autoclass:: AttributeSystem
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __add__, __sub__, __iadd__, __isub__, __getitem__, __contains__, __deepcopy__, get_power, __str__, __repr__, is_automorphic

.. automodule:: constant_assignment
 
.. autoclass:: ConstantAssignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __lt__, __getitem__, __deepcopy__, add_mapping, remove_mapping, is_total, get_domain, in_conflict, __str__, __repr__
    :inherited-members:
    :show-inheritance:

.. automodule:: context
 
.. autoclass:: Context
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __str__, __repr__, __deepcopy__, entails_formula, entails_named_state

.. automodule:: formula
 
.. autoclass:: Formula
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __str__, __repr__, __hash__, __deepcopy__, assign_truth_value

.. automodule:: interval
 
.. autoclass:: Interval
    :members:
    :private-members:
    :special-members: __init__, __lt__, __le__, __eq__, __ge__, __gt__, __ne__, __or__, __and__, __contains__, __getitem__, __deepcopy__, __hash__, discretize, __str__, __repr__, collapse_intervals

.. automodule:: named_state
 
.. autoclass:: NamedState
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __le__, add_object, is_world, get_worlds, is_named_alternate_extension, get_named_alternate_extensions, satisfies_formula, satisfies_named_state, satisfies_context, _generate_variable_assignments, is_named_entailment, is_exhaustive, __str__, __repr__
    :inherited-members:
    :show-inheritance:

.. automodule:: point
 
.. autoclass:: Point
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __getitem__, __hash__, __str__, __repr__, is_on, not_same_point, clocks_unequal, can_observe, meets, unstringify

.. automodule:: relation
 
.. autoclass:: Relation
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __iadd__, __deepcopy__, __str__, __repr__, set_definition, get_DR, set_DR, get_arity, is_valid_definition

.. automodule:: relation_symbol
 
.. autoclass:: RelationSymbol
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __hash__, __str__, __repr__

.. automodule:: state
 
.. autoclass:: State
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __deepcopy__, set_ascription, __getitem__, add_object, is_valuation, is_world, get_worlds, is_disjoint, is_alternate_extension, get_alternate_extensions, join, __str__, __repr__

.. automodule:: valueset
 
.. autoclass:: ValueSet
    :members:
    :private-members:
    :special-members: add_object_type, __init__, __eq__, __le__, __ne__, __add__, __iadd__, __sub__, __getitem__, __contains__, __len__, __iter__, __setitem__, __nonzero__, __deepcopy__, __str__, __repr__, _split_by_types, _parse

.. automodule:: variable_assignment
 
.. autoclass:: VariableAssignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __getitem__, __deepcopy__, __str__, __repr__

.. automodule:: vocabulary
 
.. autoclass:: Vocabulary
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __contains__, add_constant, add_variable, __str__, __repr__, __hash__

.. automodule:: parser_set

.. autoclass:: ParserSet
    :members:
    :private-members:
    :special-members: __init__, __len__, __getitem__, __iter__

.. automodule:: point_parser

.. autoclass:: PointParser
    :members:
    :private-members:
    :special-members: __init__, __call__, _eval

.. automodule:: truth_value_parser

.. autoclass:: TruthValueParser
    :members:
    :exclude-members: evaluate_stack, pushFirst, pushNeg, pushRel, pushUMinus
    :private-members: _eval
    :special-members: __init__, __call__

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

