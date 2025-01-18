import typing as t

from .._core import EuterpeObject
from ..note import _Note
from .schemas import TunerSchema


class _Tuner(EuterpeObject[TunerSchema]):

    _ratios: t.ClassVar[tuple[int]]
    _root: float

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is _Tuner:
            raise TypeError("Tuner cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, root: float, **kwargs):
        super().__init__(**kwargs)
        self._root = root

    def __init_subclass__(cls, *, ratios: tuple[int], reference_notenumber: int, note: type[_Note], **kwargs):
        schema = TunerSchema(
            reference_notenumber,
            note.schema,
            note.schema.pitchclass,
        )
        super().__init_subclass__(schema=schema, **kwargs)
        cls._ratios = ratios
    
    @property
    def root(self) -> float:
        return self._root

    def hz(self, notenumber: int) -> float:
        ref = notenumber - self.schema.reference_notenumber
        octnumber = ref // self.schema.pitchclass.cardinality
        pitchclass = ref % self.schema.pitchclass.cardinality
        return self._root * (2**octnumber) * self._ratios[pitchclass]

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, _Tuner):
            return NotImplemented
        return self._ratios == other._ratios

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Tuner: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Tuner: {}>".format(self.__class__.__name__)
