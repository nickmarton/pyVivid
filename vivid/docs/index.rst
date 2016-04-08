.. vivid documentation master file, created by
   sphinx-quickstart on Sun Jan 17 01:43:43 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vivid's documentation!
=================================

.. toctree::
   :maxdepth: 2

Basic Components
================

The Interval object
-------------------
.. automodule:: interval
 
.. autoclass:: Interval
    :members:
    :private-members:
    :special-members: __init__, __lt__, __le__, __eq__, __ge__, __gt__, __ne__, __or__, __and__, __contains__, __getitem__, __deepcopy__, __hash__, discretize, __str__, __repr__, collapse_intervals

The Point object
----------------
.. automodule:: point
 
.. autoclass:: Point
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __getitem__, __hash__, __str__, __repr__, is_on, not_same_point, clocks_unequal, can_observe, meets, unstringify

The LineSegment object
----------------
.. automodule:: line_segment
 
.. autoclass:: LineSegment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __ge__, __gt__, __le__, __lt__, __contains__, __deepcopy__, __getitem__, __hash__, __str__, __repr__, meets, unstringify

The ValueSet object
-------------------
.. automodule:: valueset
 
.. autoclass:: ValueSet
    :members:
    :private-members:
    :special-members: add_object_type, __init__, __eq__, __le__, __ne__, __add__, __iadd__, __sub__, __getitem__, __contains__, __len__, __iter__, __setitem__, __nonzero__, __deepcopy__, __str__, __repr__, _split_by_types, _parse

Attributes and Relations
========================

The Attribute object
--------------------
.. automodule:: attribute
 
.. autoclass:: Attribute
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __deepcopy__, __str__, __repr__, __hash__

The Relation object
--------------------
.. automodule:: relation
 
.. autoclass:: Relation
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __iadd__, __deepcopy__, __str__, __repr__, set_definition, get_DR, set_DR, get_arity, is_valid_definition

Attribute Structures
====================

The AttributeStructure object
-----------------------------
.. automodule:: attribute_structure

.. autoclass:: AttributeStructure
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __add__, __sub__, __iadd__, __isub__, __getitem__, __contains__, __deepcopy__, get_labels, get_subscripts, get_cardinality, __str__, __repr__

Attribute Systems
=================

The AttributeSystem object
--------------------------
.. automodule:: attribute_system
 
.. autoclass:: AttributeSystem
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __add__, __sub__, __iadd__, __isub__, __getitem__, __contains__, __deepcopy__, get_power, __str__, __repr__, is_automorphic

States
======

The State object
----------------
.. automodule:: state
 
.. autoclass:: State
    :members:
    :private-members:
    :special-members: __init__, __eq__, __le__, __ne__, __deepcopy__, set_ascription, __getitem__, add_object, is_valuation, is_world, get_worlds, is_disjoint, is_alternate_extension, get_alternate_extensions, join, __str__, __repr__

Vocabularies
============

The RelationSymbol object
-------------------------
.. automodule:: relation_symbol
 
.. autoclass:: RelationSymbol
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __hash__, __str__, __repr__

The Vocabulary object
---------------------
.. automodule:: vocabulary
 
.. autoclass:: Vocabulary
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __contains__, add_constant, add_variable, __str__, __repr__, __hash__

Constant and Variable Assignments
=================================

The Assignment Base Class
-------------------------
.. automodule:: assignment

.. autoclass:: Assignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__

The ConstantAssignment object
-----------------------------
.. automodule:: constant_assignment
 
.. autoclass:: ConstantAssignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __lt__, __getitem__, __deepcopy__, add_mapping, remove_mapping, is_total, get_domain, in_conflict, __str__, __repr__
    :inherited-members:
    :show-inheritance:

The VariableAssignment object
-----------------------------
.. automodule:: variable_assignment
 
.. autoclass:: VariableAssignment
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __getitem__, __deepcopy__, __str__, __repr__

Named States
============

The NamedState object
---------------------
.. automodule:: named_state
 
.. autoclass:: NamedState
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __le__, add_object, is_world, get_worlds, is_named_alternate_extension, get_named_alternate_extensions, satisfies_formula, satisfies_named_state, satisfies_context, _generate_variable_assignments, is_named_entailment, is_exhaustive, __str__, __repr__
    :show-inheritance:

Attribute Interpretations
=========================

The AttributeInterpretation object
----------------------------------
.. automodule:: attribute_interpretation
 
.. autoclass:: AttributeInterpretation
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __deepcopy__, __iter__, __str__, __repr__

Formulae and Assumption Bases
=============================

The Formula object
------------------
.. automodule:: formula
 
.. autoclass:: Formula
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __str__, __repr__, __hash__, __deepcopy__, assign_truth_value

The AssumptionBase object
-------------------------
.. automodule:: assumption_base
 
.. autoclass:: AssumptionBase
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __add__, __iadd__, __str__, __repr__, __len__, __getitem__, __iter__, __contains__, __deepcopy__

Contexts
========

The Context object
------------------
.. automodule:: context
 
.. autoclass:: Context
    :members:
    :private-members:
    :special-members: __init__, __eq__, __ne__, __str__, __repr__, __deepcopy__, entails_formula, entails_named_state

Rules of Inference for Diagrammatic Deductions
==============================================

.. currentmodule:: inference_rules

The [Thinning] Rule
-------------------
.. autofunction:: thinning

The [Widening] Rule
-------------------
.. autofunction:: widening

The [Observe] Rule
------------------
.. autofunction:: observe

The [Absurdity] Rule
--------------------
.. autofunction:: diagrammatic_absurdity

The [Diagram-Reiteration] Rule
------------------------------
.. autofunction:: diagram_reiteration

The [Sentential-to-Sentential] Rule
-----------------------------------
.. autofunction:: sentential_to_sentential

The [Diagrammatic-to-Diagrammatic] Rule
---------------------------------------
.. autofunction:: diagrammatic_to_diagrammatic

The [Sentential-to-Diagrammatic] Rule
-------------------------------------
.. autofunction:: sentential_to_diagrammatic

The [Diagrammatic-to-Sentential] Rule
-------------------------------------
.. autofunction:: diagrammatic_to_sentential

Parsers
=======

The ParserSet Object
--------------------

.. automodule:: parser_set

.. autoclass:: ParserSet
    :members:
    :private-members:
    :special-members: __init__, __len__, __getitem__, __iter__

The PointParser Object
----------------------

.. automodule:: point_parser

.. autoclass:: PointParser
    :members:
    :private-members: _eval
    :special-members: __init__, __call__

The TruthValueParser Object
---------------------------

.. automodule:: truth_value_parser

.. autoclass:: TruthValueParser
    :members:
    :exclude-members: evaluate_stack, pushFirst, pushNeg, pushRel, pushUMinus
    :private-members: _eval
    :special-members: __init__, __call__

The LineSegmentParser Object
----------------------------

.. automodule:: line_segment_parser

.. autoclass:: LineSegmentParser
    :members:
    :private-members: _eval
    :special-members: __init__, __call__