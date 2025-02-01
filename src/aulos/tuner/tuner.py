import typing as t

from aulos._core import AulosObject
from aulos.note import BaseNote

from .schemas import TunerSchema


class Tuner[NOTE: BaseNote](AulosObject[TunerSchema]):
    Note: type[NOTE]
    _ratios: t.ClassVar[tuple[float, ...]]
    _root: float

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Tuner:
            msg = "Tuner cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init__(self, root: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self._root = root

    def __init_subclass__(
        cls,
        *,
        ratios: tuple[float, ...],
        reference_notenumber: int,
        note: type[NOTE],
        **kwargs,
    ):
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
