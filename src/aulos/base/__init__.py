"""記譜体系を定義するための公開API.

``__all__`` の名前と、それらの ``_`` で始まらない属性だけが公開対象である。
具体クラスは ``Definition`` の属性に体系を束ね、文字列を生成の入口にする。
"""

from aulos.base._chord import Chord
from aulos.base._definition import Definition
from aulos.base._definition import NotationTag
from aulos.base._definition import Tag
from aulos.base._pitch import Pitch
from aulos.base._pitch import PitchClass
from aulos.base._scale import Scale
from aulos.base._structure import Voicing
from aulos.core.chain import ChainInterval
from aulos.core.chain import ChainNotation
from aulos.core.chain import Quality
from aulos.core.errors import NotationError
from aulos.core.errors import RepresentationError
from aulos.core.errors import TemperamentError
from aulos.core.notation import Comma
from aulos.core.notation import Interval
from aulos.core.notation import Notation
from aulos.core.symbols import CommaSymbols
from aulos.core.symbols import Symbols
from aulos.core.temper import Temperament
from aulos.core.temper import Tuning
from aulos.core.templates import Realization
from aulos.core.templates import Template
from aulos.core.templates import Templates

__all__ = [
    "ChainInterval",
    "ChainNotation",
    "Chord",
    "Comma",
    "CommaSymbols",
    "Definition",
    "Interval",
    "Notation",
    "NotationError",
    "NotationTag",
    "Pitch",
    "PitchClass",
    "Quality",
    "Realization",
    "RepresentationError",
    "Scale",
    "Symbols",
    "Tag",
    "Temperament",
    "TemperamentError",
    "Template",
    "Templates",
    "Tuning",
    "Voicing",
]
