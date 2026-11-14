"""テンプレートから作る音程列の定義と、根音を持たないVoicing."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from aulos.base._definition import Definition
from aulos.base._definition import require_symbol
from aulos.base._pitch import Pitch
from aulos.core.chain import ChainInterval
from aulos.core.errors import NotationError
from aulos.core.errors import RepresentationError
from aulos.core.notation import Interval
from aulos.core.templates import Realization
from aulos.core.templates import Templates

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aulos.base._definition import NotationTag


def _structure_key(intervals: Iterable[Interval]) -> tuple[tuple[int, int, tuple[tuple[int, int], ...]], ...]:
    """同じ記譜体系の中で音程列を一意に決める座標を返す."""
    return tuple((value.chain.generators, value.chain.periods, value.commas) for value in intervals)


class _StructureDefinition[N: NotationTag](Definition[N], abstract=True):
    """テンプレートから綴り付き音程列を作る定義.

    設定の注釈をdataclassのフィールド(比較・hash・reprの対象)にしないため、
    値を持つ ``_Structure`` と分けている。
    """

    pitch_type: type[Pitch[N]]
    templates: ClassVar[Templates]
    realization: ClassVar[Realization] = Realization()

    @classmethod
    def validate_definition(cls) -> None:
        """音高の型と、未使用の置換を含む全テンプレートを検証する."""
        super().validate_definition()
        cls._validate_type("pitch_type", Pitch)
        cls._validate_instance("templates", Templates)
        cls._validate_instance("realization", Realization)
        for interval, _ in cls.realization.ratios:
            cls.realization.realize(cls.notation, interval)
        for template in cls.templates.entries:
            cls.validate_intervals(cls.realization.apply(cls.notation, template))

    @classmethod
    def validate_intervals(cls, intervals: tuple[Interval[N], ...]) -> None:
        """同度を先頭とする、厳密な比の上昇列であることを検証する.

        順序は記譜上の比で判定し、束ねた調律には依存しない。
        """
        if any(not isinstance(interval, Interval) for interval in intervals):
            msg = "members must be represented by Interval objects"
            raise TypeError(msg)
        for interval in intervals:
            cls.notation.require(interval.notation)
        if not intervals or intervals[0].chain != ChainInterval(0, 0) or intervals[0].commas:
            msg = "the first interval must be the spelled unison"
            raise NotationError(msg)
        heights = [interval.ratio() for interval in intervals]
        if any(low >= high for low, high in pairwise(heights)):
            msg = "intervals must rise strictly"
            raise NotationError(msg)

    @classmethod
    def _realize(cls, name: str) -> tuple[Interval[N], ...]:
        return cls.realization.apply(cls.notation, cls.templates.get(name))


@dataclass(frozen=True, init=False, eq=False)
class _Structure[N: NotationTag](_StructureDefinition[N], abstract=True):
    """根音を持たない音程列と、登録テンプレートとの照合処理.

    等値比較は構造の種類(``kind``)と記譜上の値だけで決まり、表示規約や調律には依存しない。
    """

    kind: ClassVar[str]
    """Voicing・Chord・Scaleを区別する名前。種類が異なる構造は等しくならない."""
    intervals: tuple[Interval[N], ...]

    def _identity(self) -> tuple[object, ...]:
        return (self.kind, self.intervals)

    def __eq__(self, other: object) -> bool:
        """種類と記譜上の値が等しいか判定する."""
        if not isinstance(other, _Structure):
            return NotImplemented
        return self._identity() == other._identity()

    def __hash__(self) -> int:
        """種類と記譜上の値からhashを作る."""
        return hash(self._identity())

    @property
    def template_name(self) -> str:
        """比まで一致する最初のテンプレート名を返す。未登録構造は拒否する.

        コンマの数も照合するため、綴りが同じでも規約と異なる比の構造には名前を返さない。
        """
        structure = _structure_key(self.intervals)
        for template in self.templates.entries:
            if _structure_key(self.realization.apply(self.notation, template)) == structure:
                return template.name
        msg = "no template represents these spelled intervals"
        raise RepresentationError(msg)

    @property
    def structure_name(self) -> str:
        """コンマを除いた綴りが一致する最初のテンプレート名を返す。未登録構造は拒否する.

        比の選び方によらず、文字と変化量だけで構造を照合する。
        """
        spelled = tuple(interval.chain for interval in self.intervals)
        for template in self.templates.entries:
            if template.intervals == spelled:
                return template.name
        msg = "no template spells these intervals"
        raise RepresentationError(msg)


class Voicing[N: NotationTag](_Structure[N], abstract=True):
    """根音を持たない音程列。複数周期にまたがり、同じ音高クラスを重複できる."""

    kind = "voicing"

    def __init__(self, name: str) -> None:
        """テンプレート名から生成する."""
        self._require_concrete()
        require_symbol(name)
        self._initialize(self._realize(name))

    def _initialize(self, intervals: Iterable[Interval[N]]) -> None:
        self._require_concrete()
        values = tuple(intervals)
        self.validate_intervals(values)
        object.__setattr__(self, "intervals", values)

    @classmethod
    def from_intervals(cls, intervals: Iterable[Interval[N]]) -> Self:
        """同度を先頭とする、比が厳密に上昇する綴り付き音程列を検証して生成する."""
        result = object.__new__(cls)
        result._initialize(intervals)
        return result

    def at(self, root: Pitch[N]) -> tuple[Pitch[N], ...]:
        """``root`` を根音とする音高列を返す."""
        if not isinstance(root, Pitch):
            msg = "a voicing needs a Pitch root"
            raise TypeError(msg)
        self.notation.require(root.notation)
        bound = self.pitch_type._wrap(root._value)
        return tuple(bound + interval for interval in self.intervals)

    def __str__(self) -> str:
        """登録構造のテンプレート名を返す."""
        return self.template_name
