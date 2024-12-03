import typing as t


def is_coexistancable(value: t.Any) -> t.TypeGuard[dict]:
    return isinstance(value, dict) and 0 < len(value)


class Coexistence:
    """
    A class for managing coexistence of hashable objects stored in dictionaries at the instance and class levels.

    Attributes:
        _i_coexistence (dict[str, Hashable]): An instance-level dictionary containing hashable objects for coexistence.
        _t_coexistence (ClassVar[dict[str, Hashable]]): A class-level dictionary containing hashable objects for coexistence.

    Methods:
        __init__(**coexistencable: Hashable): Initializes the instance with keyword arguments representing hashable objects.
        __init_subclass__(**coexistencable: Hashable): Initializes subclasses with keyword arguments representing hashable objects.
        canCoexist(other: Self) -> bool: Determines whether two Coexistence objects can coexist based on their hash values.
    """

    _i_coexistence: dict[str, t.Hashable]
    _t_coexistence: t.ClassVar[dict[str, t.Hashable]]

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

        Coexistence is determined by comparing the hash values of their instance-level (_i_coexistence)
        or class-level (_t_coexistence) coexistence dictionaries.

        Args:
            other (Self): Another Coexistence object to compare against.

        Returns:
            bool: True if the two objects can coexist (their hash values are equal); otherwise, False.
        """
        return hash(self._i_coexistence or self._t_coexistence) == hash(
            other._i_coexistence or other._t_coexistence
        )
