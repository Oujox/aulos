import typing as t

from .._core import EuterpeObject


class Tuner(EuterpeObject):

    _ratios: t.ClassVar[tuple[int]]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Tuner:
            raise TypeError("Tuner cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __init_subclass__(cls, ratios: tuple[int], **kwargs):
        cls._ratios = ratios
        return super().__init_subclass__(**kwargs)

    def hz(self, notenumber: int) -> float:
        rel = notenumber - self.schema.root_notenumber
        octnumber = rel // self.schema.semitone
        pitchclass = rel % self.schema.semitone
        return self.schema.root_hz * (2**octnumber) * self._ratios[pitchclass]

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Tuner):
            return NotImplemented
        return self._ratios == other._ratios

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Tuner: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Tuner: {}>".format(self.__class__.__name__)
