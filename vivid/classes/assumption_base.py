"""assumption_base module."""

from formula import Formula


class AssumptionBase(object):
    """
    AssumptionBase class.

    This class functions as a container for a finite set of Formulae over a
    single Vocabulary, i.e., :math:`\\beta`.

    :ivar formulae: The set of Formula objects contained in the \
    AssumptionBase object.
    :ivar vocabulary: The underlying Vocabulary object the AssumptionBase is \
    defined over.
    :ivar _is_AssumptionBase: An identifier to use in place of type or \
    isinstance.
    """

    def __init__(self, *formulae):
        """
        Construct an AssumptionBase object.

        :param formulae: Any amount of Formula objects or a single Vocabulary \
        object if AssumptionBase no Formula objects are provided.
        :type  formulae: Formula|Vocabulary

        :raises TypeError: All optional positional arguments provided must be \
        Formula objects or only a single Vocabulary object may be provided.
        :raises ValueError: All Formula objects provided as optional \
        positional arguments must share the same Vocabulary.
        """

        self._formulae = []

        if formulae:
            if len(formulae) == 1 and hasattr(formulae[0], "_is_Vocabulary"):
                self._vocabulary = formulae[0]
            else:
                # Ensure all optional positional args are of type Formula.
                for f in formulae:
                    if not hasattr(f, "_is_Formula"):
                        raise TypeError(
                            "all arguments passed to constructor must be a "
                            "Formula object")

                # check for same vocabulary condition and add formula to list
                vocabulary = formulae[0]._vocabulary
                names = [f._name for f in formulae]

                if len(names) != len(set(names)):
                    raise ValueError("Duplicate Formula names not permitted")

                for f in formulae:
                    if vocabulary is not f._vocabulary:
                        raise ValueError(
                            "all formulae provided to constructor must share "
                            "the same Vocabulary")

                    # ensure no duplicates
                    if f not in self._formulae:
                        self._formulae.append(f)

                self._formulae = sorted(self._formulae, key=lambda x: x._name)
                self._vocabulary = vocabulary

        else:
            raise TypeError(
                "AssumptionBase require either a Vocabulary or at least 1 "
                "Formula")

        self._is_AssumptionBase = True

    def __eq__(self, other):
        """
        Determine if two AssumptionBase objects are equal via the ``==``
        operator.
        """

        if not hasattr(other, "_is_AssumptionBase"):
            raise TypeError(
                "Can only compare an AssumptionBase object with "
                "another AssumptionBase object")

        # Cardinalities must be the same.
        if len(self._formulae) != len(other._formulae):
            return False

        if self._vocabulary is not other._vocabulary:
            return False

        # check if each formula in self has a match in other.
        intersection = set(self._formulae) & set(other._formulae)
        union = set(self._formulae) | set(other._formulae)
        return intersection == union

    def __ne__(self, other):
        """
        Determine if two AssumptionBase objects are not equal via the ``!=``
        operator.
        """

        return not self.__eq__(other)

    def __add__(self, other):
        """
        Add all Formula objects in another AssumptionBase or a single Formula
        object to an AssumptionBase object via the ``+`` operator.

        :raises TypeError: Only Formula or AssumptionBase objects can be \
        added to an AssumptionBase object.
        :raises ValueError: Cannot add objects with different underlying \
        Vocabulary objects and duplicate Formula objects are not permitted.
        """

        from copy import deepcopy
        self_copy = deepcopy(self)

        # Handle adding an AssumptionBase
        if hasattr(other, "_is_AssumptionBase"):
            # Edge cases
            if len(self) == 0:
                return deepcopy(other)
            if len(other) == 0:
                return self_copy

            names = [formula._name for formula in self._formulae]
            vocabulary = self._formulae[0]._vocabulary

            for other_formula in other:
                if other_formula._vocabulary != vocabulary:
                    raise ValueError(
                        "Cannot add AssumptionBase's with different "
                        "Vocabulary's")
                if other_formula._name in names:
                    raise ValueError("Duplicate Formula objects not permitted")

                self_copy._formulae.append(deepcopy(other_formula))

            self_copy._formulae = sorted(self_copy._formulae,
                                         key=lambda x: x._name)

            return self_copy

        # Handle adding a Formula
        if hasattr(other, "_is_Formula"):
            # Edge cases
            if len(self) == 0:
                if other._vocabulary is not self._vocabulary:
                    raise ValueError(
                        "Cannot add Formula's with different Vocabulary's")

                return AssumptionBase(*deepcopy([other]))

            names = [formula._name for formula in self._formulae]

            if other._vocabulary is not self._vocabulary:
                raise ValueError(
                    "Cannot add Formula's with different Vocabulary's")
            if other._name in names:
                raise ValueError("Duplicate Formula objects not permitted")

            self_copy._formulae.append(deepcopy(other))
            self_copy._formulae = sorted(self_copy._formulae,
                                         key=lambda x: x._name)

            return self_copy

        raise TypeError(
            "Only Formula and AssumptionBase objects can be added to an "
            "AssumptionBase")

    def __iadd__(self, other):
        """
        Add all Formula objects in another AssumptionBase or a single Formula
        object to this AssumptionBase object via the ``+`` operator.

        :raises TypeError: Only Formula or AssumptionBase objects can be \
        added to an AssumptionBase object.
        :raises ValueError: Cannot add objects with different underlying \
        Vocabulary objects and duplicate Formula objects are not permitted.
        """

        return self + other

    def __str__(self):
        """
        Return a readable string representation of the AssumptionBase object.
        """

        return 'AB(' + ', '.join([str(f) for f in self._formulae]) + ')'

    def __repr__(self):
        """
        Return a string representation of the AssumptionBase object.
        """

        return self.__str__()

    def __len__(self):
        """
        Determine the length of an AssumptionBase object via the ``len``
        built-in function e.g.(``len(AssumptionBase)``).
        """

        return len(self._formulae)

    def __getitem__(self, key):
        """
        Retrive the Formula correspond to key given by ``key`` parameter via
        indexing (e.g. ``AssumptionBase[key]``).

        :param key: The key to use for indexing a Formula in the \
        AssumptionBase.
        :type  key: ``int`` | ``str`` | Formula

        :raises IndexError: ``int`` key is out of range.
        :raises KeyError: ``key`` parameter does not correspond to any \
        Formula object in the AssumptionBase.
        :raises TypeError: ``key`` parameter must be an ``int``, ``str``, or \
        Formula object.
        """

        if hasattr(key, "_is_Formula"):
            for i, formula in enumerate(self._formulae):
                if key == formula:
                    return self._formulae[i]
            raise KeyError("Formula not found")

        if isinstance(key, str):
            for i, name in enumerate([f._name for f in self._formulae]):
                if key == name:
                    return self._formulae[i]
            raise KeyError("Formula not found")

        if isinstance(key, int):
            try:
                return self._formulae[key]
            except IndexError:
                raise IndexError(
                    str(key) + " not a valid index in AssumptionBase")

        raise TypeError("Invalid key type")

    def __iter__(self):
        """
        Provides an iterator for AssumptionBase
        (e.g. \"``for formula in AssumptionBase:``\").
        """

        for formula in self._formulae:
            yield formula

    def __contains__(self, item):
        """
        Overloaded ``in`` operator for AssumptionBase. Determine if a formula
        is contained in this AssumptionBase object.

        :param key: The Formula object or name of Formula object to test for \
        membership in this AssumptionBase.
        :type  key: Formula | ``str``
        """

        # Handle if item provided is a string; assume it's a Formula name
        if type(item) == str:
            names = [f._name for f in self._formulae]
            if item in names:
                return True

        # Handle if Formula object is provided
        if hasattr(item, "_is_Formula"):
            for formula in self._formulae:
                if item == formula:
                    return True

        return False

    def __deepcopy__(self, memo):
        """
        Deepcopy an AssumptionBase object via the ``copy.deepcopy`` method.
        This does not break the reference to the underlying Vocabulary object.
        """

        from copy import deepcopy
        # If the AssumptionBase has any formulae, copy like normal.
        # Otherwise, it's empty so we need to pass the Vocabulary
        if self._formulae:
            return AssumptionBase(*deepcopy(self._formulae))
        else:
            return AssumptionBase(self._vocabulary)


def main():
    """Quick tests."""
    from relationsymbol import RelationSymbol
    from vocabulary import Vocabulary

    ahead_rs = RelationSymbol('Ahead', 4)
    behind_rs = RelationSymbol('Behind', 4)
    pm_rs = RelationSymbol('PM', 1)
    vocabulary = Vocabulary(
        ['C1', 'C2'], [ahead_rs, behind_rs, pm_rs], ['V1', 'V2'])

    f1 = Formula(vocabulary, 'Ahead', 'C1', 'V1')
    f2 = Formula(vocabulary, 'Behind', 'C1')

    a = AssumptionBase(f1, f2)
    a2 = AssumptionBase(f2, f1)

    print a2

if __name__ == "__main__":
    main()
