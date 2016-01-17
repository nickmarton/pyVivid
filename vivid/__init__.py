"""Vivid package."""

from vivid.classes.assumption_base import AssumptionBase
from vivid.classes.attribute import Attribute
from vivid.classes.attribute_interpretation import AttributeInterpretation
from vivid.classes.attribute_structure import AttributeStructure
from vivid.classes.attribute_system import AttributeSystem
from vivid.classes.constant_assignment import ConstantAssignment
from vivid.classes.context import Context
from vivid.classes.formula import Formula
from vivid.classes.interval import Interval
from vivid.classes.named_state import NamedState
from vivid.classes.point import Point
from vivid.classes.relation import Relation
from vivid.classes.relation_symbol import RelationSymbol
from vivid.classes.state import State
from vivid.classes.valueset import ValueSet
from vivid.classes.variable_assignment import VariableAssignment
from vivid.classes.vocabulary import Vocabulary

from vivid.classes.inference_rules import thinning, widening, observe
from vivid.classes.inference_rules import diagrammatic_absurdity
from vivid.classes.inference_rules import sentential_absurdity
from vivid.classes.inference_rules import diagram_reiteration
from vivid.classes.inference_rules import sentential_to_sentential
from vivid.classes.inference_rules import diagrammatic_to_diagrammatic
from vivid.classes.inference_rules import sentential_to_diagrammatic
from vivid.classes.inference_rules import diagrammatic_to_sentential
