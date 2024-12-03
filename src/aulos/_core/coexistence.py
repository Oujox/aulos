import typing as t


def is_coexistancable(value: t.Any) -> t.TypeGuard[dict]:
    return isinstance(value, dict) and 0 < len(value)


class Coexistence:
    """
    A class for managing coexistence of hashable objects stored in dictionaries at the instance and class levels.

    This class allows for defining hashable dictionaries at both the instance and class levels,
    and provides a method to check whether two Coexistence objects can coexist based on their values.

    Attributes:
        _i_coexistence (Optional[dict[str, Hashable]]): An instance-level dictionary containing hashable objects for coexistence.
        _t_coexistence (ClassVar[Optional[dict[str, Hashable]]]): A class-level dictionary containing hashable objects for coexistence.

    Methods:
        __init__(**coexistencable: Hashable): Initializes the instance with keyword arguments representing hashable objects stored in a dictionary.
        __init_subclass__(**coexistencable: Hashable): Initializes the subclass with keyword arguments representing hashable objects stored in a dictionary.
        canCoexist(other: Self) -> bool: Determines whether two Coexistence objects can coexist based on the equality of their dictionaries.
    """

    _i_coexistence: t.Optional[dict[str, t.Hashable]]
    _t_coexistence: t.ClassVar[t.Optional[dict[str, t.Hashable]]]

    def __init__(self, /, **coexistencable: t.Hashable) -> None:
        self._i_coexistence = (
            coexistencable if is_coexistancable(coexistencable) else None
        )
        return super(Coexistence, self).__init__()

    def __init_subclass__(cls, /, **coexistencable: t.Hashable) -> None:
        cls._t_coexistence = (
            coexistencable if is_coexistancable(coexistencable) else None
        )
        return super(Coexistence, cls).__init_subclass__()

    def canCoexist(self, other: t.Self) -> bool:
        """
        Determines whether two Coexistence objects can coexist.

        Coexistence is determined by comparing the equality of the dictionaries of hashable objects
        stored at the instance (_i_coexistence) or class (_t_coexistence) levels.

        Args:
            other (Self): Another Coexistence object to compare against.

        Returns:
            bool: True if the two objects can coexist (their dictionaries are equal); otherwise, False.
        """
        return (self._t_coexistence or self._i_coexistence) == (
            other._t_coexistence or other._i_coexistence
        )
