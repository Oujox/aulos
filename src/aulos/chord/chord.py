import typing as t

from .._core import AulosObject
from ._base import BaseChord


class Chord(BaseChord, AulosObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
