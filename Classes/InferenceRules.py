"""This module intends to provide the rules of diagrammatic inference."""


def widening(context, named_state):
    """
    Verify that NamedState named_state can be obtained from Context context by
    widening.
    """

    if not hasattr(context, "_is_Context"):
        raise TypeError("context parameter must be a Context object.")

    if not hasattr(named_state, "_is_NamedState"):
        raise TypeError("named_state parameter must be a NamedState object.")

    return context._named_state <= named_state


def diagram_reiteration(context, named_state=None):
    """Perform Diagram Reiteration to retrieve the current diagram."""
    if named_state:
        if not hasattr(named_state, "_is_NamedState"):
            raise TypeError(
                "named_state parameter must be a NamedState object")
            if context._named_state != named_state:
                raise ValueError(
                    "named_state parameter must match NamedState object "
                    "within Context context")

            return named_state

    return context._named_state


def main():
    """dev tests."""
    pass


if __name__ == "__main__":
    main()
