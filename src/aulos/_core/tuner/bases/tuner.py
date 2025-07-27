import typing as t
from typing import cast

from aulos._core.context import inject
from aulos._core.note import BaseNote
from aulos._core.object import AulosSchemaObject
from aulos._core.utils import classproperty

from ..schemas import TunerSchema


class BaseTuner[NOTE: BaseNote](AulosSchemaObject[TunerSchema]):
    """
    Represents a musical tuner that can convert note numbers to their corresponding
    frequencies in hertz (Hz) based on a specified tuning system.

    This class provides methods to handle different tuning systems, allowing for
    the conversion of musical notes into precise frequencies. It supports various tuning ratios
    and reference note numbers, making it versatile for different musical contexts.
    """

    _Note: t.ClassVar[type[BaseNote]]
    _ratios: t.ClassVar[tuple[float, ...]]

    _root: float

    @inject
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
        cls._Note = note
        cls._ratios = ratios

    @classproperty
    def Note(self) -> type[NOTE]:  # noqa: N802
        """The type of note associated with the tuner."""
        return cast("type[NOTE]", self._Note)

    @classproperty
    def ratios(self) -> tuple[float, ...]:
        """The tuning ratios used to calculate frequencies."""
        return self._ratios

    @property
    def root(self) -> float:
        """Returns the root frequency of the tuner."""
        return self._root

    def hz(self, notenumber: int) -> float:
        """Converts a note number to its corresponding frequency in hertz."""
        ref = notenumber - self.schema.reference_notenumber
        octnumber = ref // self.schema.pitchclass.classes
        pitchclass = ref % self.schema.pitchclass.classes
        return self._root * (2**octnumber) * self.ratios[pitchclass]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseTuner):
            return NotImplemented
        return self.ratios == other.ratios

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"

    def __repr__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"
