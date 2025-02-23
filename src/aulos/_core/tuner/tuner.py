import typing as t

from aulos._core.note import BaseNote
from aulos._core.object import AulosObject

from .schemas import TunerSchema


class Tuner[NOTE: BaseNote](AulosObject[TunerSchema]):
    """
    Represents a musical tuner that can convert note numbers to their corresponding
    frequencies in hertz (Hz) based on a specified tuning system.

    This class provides methods to handle different tuning systems, allowing for
    the conversion of musical notes into precise frequencies. It supports various tuning ratios
    and reference note numbers, making it versatile for different musical contexts.
    """

    Note: type[NOTE]
    """The type of note associated with the tuner."""

    ratios: t.ClassVar[tuple[float, ...]]
    """The tuning ratios used to calculate frequencies."""

    _root: float

    def __init__(self, root: float, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._root = root

    def __init_subclass__(
        cls,
        *,
        ratios: tuple[float, ...],
        reference_notenumber: int,
        note: type[NOTE],
        **kwargs: t.Any,
    ) -> None:
        schema = TunerSchema(
            reference_notenumber,
            note.schema,
            note.schema.pitchclass,
        )
        super().__init_subclass__(schema=schema, **kwargs)
        cls.Note = note
        cls.ratios = ratios

    @property
    def root(self) -> float:
        """Returns the root frequency of the tuner."""
        return self._root

    def hz(self, notenumber: int) -> float:
        """Converts a note number to its corresponding frequency in hertz."""
        ref = notenumber - self.schema.reference_notenumber
        octnumber = ref // self.schema.pitchclass.cardinality
        pitchclass = ref % self.schema.pitchclass.cardinality
        return self._root * (2**octnumber) * self.ratios[pitchclass]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tuner):
            return NotImplemented
        return self.ratios == other.ratios

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"

    def __repr__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"
