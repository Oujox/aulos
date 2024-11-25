import typing as t


def is_semitone(value: t.Any) -> t.TypeGuard[int]:
    return isinstance(value, int) and 0 <= value


class HarmonicSystem:
    """
    A base class representing a harmonic system (musical temperament).

    This class is designed to specify the temperament (number of semitones) associated with musical objects
    such as note names or scales. It clarifies the harmonic context these objects operate within and ensures
    consistent behavior across the music theory library.

    Attributes:
        _i_semitone (Optional[int]): The temperament specified at the instance level, if valid.
        _t_semitone (ClassVar[Optional[int]]): The temperament specified at the class level during subclass definition, if valid.

    Purpose:
    - To ensure that each musical object operates within the appropriate harmonic context.
    - To unify shared characteristics across temperaments based on the same semitone count, such as 12-tone equal temperament,
      Pythagorean tuning, or just intonation.

    Example Use Case:
    If the `semitone` property of an object is 12, it indicates the object is based on a harmonic system with 12 semitones,
    such as 12-tone equal temperament, Pythagorean tuning, or just intonation.

    Methods:
        __init__: Initializes the instance with a specified temperament, if valid.
        __init_subclass__: Sets the class-wide temperament during subclass definition.
        semitone (property): Returns the active temperament in semitones, prioritizing class-level over instance-level values.
    """

    _i_semitone: t.Optional[int]
    _t_semitone: t.ClassVar[t.Optional[int]]

    def __init__(self, semitone: t.Optional[int] = None) -> None:
        self._i_semitone = semitone if is_semitone(semitone) else None
        return super(HarmonicSystem, self).__init__()

    def __init_subclass__(cls, semitone: t.Optional[int] = None) -> None:
        cls._t_semitone = semitone if is_semitone(semitone) else None
        return super(HarmonicSystem, cls).__init_subclass__()

    @property
    def semitone(self) -> int:
        """
        Returns the active temperament's semitone count.

        The semitone count is determined by the following priority:
        1. The class-level temperament (_t_semitone) set during subclass definition.
        2. The instance-level temperament (_i_semitone) set during object initialization.
        3. Defaults to 0 if neither is specified.

        This property provides a unified way to access the harmonic system's semitone value,
        ensuring consistent behavior across instances and subclasses.

        Returns:
            int: The semitone count representing the active harmonic system.
        """
        return self._t_semitone or self._i_semitone or 0
