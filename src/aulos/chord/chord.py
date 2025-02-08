import typing as t

from aulos._core import AulosObject
from aulos.note import BaseNote

from .quality import Quality, QualityProperty
from .schemas import ChordSchema


class BaseChord[NOTE: BaseNote](AulosObject[ChordSchema]):
    Note: type[NOTE]
    _name: str

    def __init__(self, name: str, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._name = name

    def __init_subclass__(cls, qualities: t.Sequence[QualityProperty], note: type[NOTE]) -> None:
        schema = ChordSchema(
            tuple(Quality(**q) for q in qualities),
        )
        super().__init_subclass__(schema=schema)
        cls.Note = note

    @classmethod
    def is_chordname(cls, chordname: object) -> t.TypeGuard[str]:
        return isinstance(chordname, str)
