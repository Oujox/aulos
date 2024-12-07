import typing as t


def is_hashable(*value: t.Hashable) -> t.TypeGuard[dict]:
    return all(hasattr(v, "__hash__") for v in value) and 0 < len(value)


class Coexistence:
    """
    A base class for managing coexistence conditions between objects.

    The `Coexistence` class allows for defining and comparing hashable attributes
    for both instance-level (`_i_coexistence`) and subclass-level (`_t_coexistence`)
    coexistence requirements. Objects of this class can determine if they can
    coexist with other instances or subclasses by comparing their respective
    coexistence attributes.

    Attributes:
        _i_coexistence (Optional[frozenset[Hashable]]): A frozenset representing
            hashable coexistence items at the instance level. If the provided
            attributes are not hashable, this will be set to `None`.
        _t_coexistence (ClassVar[Optional[frozenset[Hashable]]]): A frozenset
            representing hashable coexistence items at the class level. This is
            shared among all instances of a specific subclass.

    Methods:
        canCoexist(other: Self) -> bool:
            Determines whether the current instance can coexist with another
            instance or subclass by comparing their `_i_coexistence` or
            `_t_coexistence` attributes.

    Special Methods:
        __init__(**coexistencable: Hashable):
            Initializes an instance with hashable attributes for coexistence.
            If the attributes are not hashable, `_i_coexistence` is set to `None`.

        __init_subclass__(cls, **coexistencable: Hashable):
            Initializes a subclass with hashable attributes for coexistence.
            If the attributes are not hashable, `_t_coexistence` is set to `None`.

    Example:
        class SubClass(Coexistence, coexistencable={"key": "value"}):
            pass

        instance1 = Coexistence(key="value")
        instance2 = Coexistence(key="value")
        print(instance1.canCoexist(instance2))  # Output: True

    Notes:
        - The `is_hashable` function is expected to determine if the given values
          are hashable.
        - The `coexistencable` keyword arguments must contain hashable values
          for the `_i_coexistence` or `_t_coexistence` attributes to be set.
    """

    _i_coexistence: t.Optional[frozenset[t.Hashable]]
    _t_coexistence: t.ClassVar[t.Optional[frozenset[t.Hashable]]]

    def __init__(self, **coexistencable: t.Hashable) -> None:
        self._i_coexistence = (
            frozenset(coexistencable.items())
            if is_hashable(*coexistencable.values())
            else None
        )
        return super(Coexistence, self).__init__()

    def __init_subclass__(cls, **coexistencable: t.Hashable) -> None:
        cls._t_coexistence = (
            frozenset(coexistencable.items())
            if is_hashable(coexistencable.values())
            else None
        )
        return super(Coexistence, cls).__init_subclass__()

    def can_coexist(self, other: t.Self) -> bool:
        return (self._t_coexistence or self._i_coexistence) == (
            other._t_coexistence or other._i_coexistence
        )
