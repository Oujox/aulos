"""音名から生成する音高クラスと音高."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Self
from typing import overload

from aulos.base._definition import Definition
from aulos.base._definition import require_symbol
from aulos.core.notation import Interval
from aulos.core.pitch import PitchClassValue
from aulos.core.pitch import PitchValue

if TYPE_CHECKING:
    from fractions import Fraction

    from aulos.base._definition import NotationTag
    from aulos.core.symbols import Symbols
    from aulos.core.temper import Tuning


@dataclass(frozen=True, init=False, eq=False)
class PitchClass[N: NotationTag](Definition[N], abstract=True):
    """音域を持たない綴り。調律後の異名同音も区別する.

    等値比較は記譜体系と綴りだけで決まり、具体クラスが束ねる表示規約や調律には依存しない。
    """

    _value: PitchClassValue[N]

    def __init__(self, symbol: str) -> None:
        """``"C#"`` のような音域なしの音名から生成する."""
        self._require_concrete()
        require_symbol(symbol)
        letter, alteration, commas = self.symbols._parse_class(symbol)
        object.__setattr__(self, "_value", PitchClassValue(self.notation, letter, alteration, commas))

    @classmethod
    def _wrap(cls, value: PitchClassValue[N]) -> Self:
        cls._require_concrete()
        made = object.__new__(cls)
        object.__setattr__(made, "_value", value)
        return made

    @classmethod
    def from_spelling(cls, letter: int, alteration: int = 0, commas: tuple[tuple[int, int], ...] = ()) -> Self:
        """文字位置・変化量・素数ごとのコンマ数から生成する.

        ``letter`` は ``symbols.letters`` の0始まりの位置、``commas`` は
        ``(素数, 符号付きの回数)`` の列。重複した素数の回数は合算する。
        """
        cls._require_concrete()
        return cls._wrap(PitchClassValue(cls.notation, letter, alteration, commas))

    @property
    def letter(self) -> int:
        """``symbols.letters`` における0始まりの文字位置を返す."""
        return self._value.letter

    @property
    def alteration(self) -> int:
        """変化量を返す."""
        return self._value.alteration

    @property
    def commas(self) -> tuple[tuple[int, int], ...]:
        """素数ごとのコンマ数を返す."""
        return self._value.commas

    def __add__(self, interval: Interval[N]) -> Self:
        """移調する。音域の変化は捨てる."""
        if not isinstance(interval, Interval):
            return NotImplemented
        return self._wrap(self._value + interval)

    def __sub__(self, interval: Interval[N]) -> Self:
        """音程を引いて移調する."""
        if not isinstance(interval, Interval):
            return NotImplemented
        return self._wrap(self._value - interval)

    def __eq__(self, other: object) -> bool:
        """記譜上の値が等しいか判定する。表示規約や束ねた調律の違いは区別しない."""
        if not isinstance(other, PitchClass):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        """記譜上の値からhashを作る."""
        return hash(self._value)

    def __str__(self) -> str:
        """音域なしの音名を返す."""
        return self._render(self.symbols)

    def _render(self, symbols: Symbols) -> str:
        value = self._value
        return symbols._render_class(value.letter, value.alteration, value.commas)


class _PitchDefinition[N: NotationTag](Definition[N], abstract=True):
    """関連する型の設定を、値を持つ ``Pitch`` のdataclassフィールドにしないための中間クラス."""

    pitch_class_type: type[PitchClass[N]]


@dataclass(frozen=True, init=False, eq=False)
class Pitch[N: NotationTag](_PitchDefinition[N], abstract=True):
    """綴り付き音高クラスと内部音域からなる音高.

    等値比較は記譜体系と綴りだけで決まり、具体クラスが束ねる表示規約や調律には依存しない。
    """

    _value: PitchValue[N]

    def __init__(self, symbol: str) -> None:
        """``"C#4"`` のような音名から生成する."""
        self._require_concrete()
        require_symbol(symbol)
        spelling, commas = self.symbols._parse_pitch(symbol)
        object.__setattr__(self, "_value", PitchValue.of(self.notation, spelling, commas))

    @classmethod
    def validate_definition(cls) -> None:
        """音高クラスの型が同じ体系であることも検証する."""
        super().validate_definition()
        cls._validate_type("pitch_class_type", PitchClass)

    @classmethod
    def _wrap(cls, value: PitchValue[N]) -> Self:
        cls._require_concrete()
        made = object.__new__(cls)
        object.__setattr__(made, "_value", value)
        return made

    @classmethod
    def from_class(cls, pitch_class: PitchClass[N], register: int = 0) -> Self:
        """同じ記譜体系の音高クラスと内部音域から生成する.

        ``register`` は原点の文字から数えた周期数で、表示上の音域番号ではない。
        """
        if not isinstance(pitch_class, PitchClass):
            msg = "a pitch needs a PitchClass"
            raise TypeError(msg)
        cls._require_concrete()
        cls.notation.require(pitch_class.notation)
        return cls._wrap(pitch_class._value.at(register))

    @property
    def pitch_class(self) -> PitchClass[N]:
        """音域を除いた音高クラスを返す."""
        return self.pitch_class_type._wrap(self._value.pitch_class)

    @property
    def register(self) -> int:
        """原点の文字から数えた内部音域を返す。表示上の番号とは異なる."""
        return self._value.register

    def ratio(self) -> Fraction:
        """体系の原点に対する正確な比を返す。調律は適用しない."""
        return self._value.ratio()

    def frequency(self, anchor: Pitch[N], anchor_hz: float, tuning: Tuning | None = None) -> float:
        """基準音 ``anchor`` の周波数 ``anchor_hz`` から、自身の周波数をHzで返す.

        基準音は同じ記譜体系で、基準周波数は正の有限値でなければならない。
        ``tuning`` の省略時は束ねた調律を使い、調律を束ねない型では指定が必要。
        """
        return self._resolve_tuning(tuning).frequency((self - anchor).ratio(), anchor_hz)

    def enharmonics(self, tuning: Tuning | None = None, most: int | None = None) -> tuple[Self, ...]:
        """等分律で同じ高さになる、コンマを持たない別の綴りを返す.

        変化記号が ``most`` 個以下(省略時は表示規約の上限)の綴りを、変化記号の少ない順に並べる。
        ``tuning`` の省略時は束ねた調律を使う。生成音程が一つの調律にだけ対応し、
        それ以外の調律や、文字の順序を保たない調律は拒否する。
        """
        temperament = self._resolve_tuning(tuning).temperament
        limit = self.symbols.most if most is None else most
        if type(limit) is not int:
            msg = "the alteration limit must be an integer"
            raise TypeError(msg)
        chain = self.notation.chain
        points = temperament._spellings(chain, temperament.map(self.ratio())[0], limit)
        values = (PitchValue.of(self.notation, chain._spell(point)) for point in points)
        return tuple(self._wrap(value) for value in values if value != self._value)

    def __add__(self, interval: Interval[N]) -> Self:
        """音程を加える."""
        if not isinstance(interval, Interval):
            return NotImplemented
        return self._wrap(self._value + interval)

    @overload
    def __sub__(self, other: Pitch[N]) -> Interval[N]: ...

    @overload
    def __sub__(self, other: Interval[N]) -> Self: ...

    def __sub__(self, other: Pitch[N] | Interval[N]) -> Interval[N] | Self:
        """音高間の音程、または音程を引いた音高を返す."""
        if isinstance(other, Interval):
            return self._wrap(self._value - other)
        if isinstance(other, Pitch):
            return self._value - other._value
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        """記譜上の値が等しいか判定する。表示規約や束ねた調律の違いは区別しない."""
        if not isinstance(other, Pitch):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        """記譜上の値からhashを作る."""
        return hash(self._value)

    def __str__(self) -> str:
        """音域番号とコンマ記号を含む音名を返す."""
        return self._render(self.symbols)

    def _render(self, symbols: Symbols) -> str:
        return symbols._render_pitch(self._value.spelling, self._value.pitch_class.commas)
