import typing as t

from aulos._core import AulosObject
from aulos.note import BaseNote

from .schemas import TunerSchema


class Tuner[NOTE: BaseNote](AulosObject[TunerSchema]):
    """
    Tuner class for tuning musical notes.

    Attributes:
        Note (type[NOTE]): The note type used by the tuner.
        _ratios (ClassVar[tuple[float, ...]]): The tuning ratios.
        _root (float): The root frequency.
    """

    Note: type[NOTE]
    _ratios: t.ClassVar[tuple[float, ...]]
    _root: float

    __slots__ = ("_root",)

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
        cls._ratios = ratios

    @property
    def root(self) -> float:
        return self._root

    def hz(self, notenumber: int) -> float:
        ref = notenumber - self.schema.reference_notenumber
        octnumber = ref // self.schema.pitchclass.cardinality
        pitchclass = ref % self.schema.pitchclass.cardinality
        return self._root * (2**octnumber) * self._ratios[pitchclass]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tuner):
            return NotImplemented
        return self._ratios == other._ratios

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"

    def __repr__(self) -> str:
        return f"<Tuner: {self.__class__.__name__}>"
