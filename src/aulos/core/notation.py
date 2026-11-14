"""記譜体系と、体系に結び付いた音程.

型引数は用途の分類であり、体系の一致は実行時に定義の値を比較して確かめる。
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import Self

from aulos.core.chain import ChainInterval
from aulos.core.chain import ChainNotation
from aulos.core.chain import Quality
from aulos.core.errors import NotationError
from aulos.core.maths import is_prime
from aulos.core.monzo import Monzo

if TYPE_CHECKING:
    from aulos.core.temper import Tuning


@dataclass(frozen=True, slots=True)
class Comma:
    """連鎖の外の素数を綴るためのコンマ規約.

    ``prime`` は対象の素数、``ratio`` はその指数が+1または-1となる正の有理比。
    連鎖から独立しているかは ``Notation`` に束ねる時に検証する。
    """

    prime: int
    ratio: Fraction | int
    _monzo: Monzo = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if type(self.prime) is not int or not isinstance(self.ratio, (int, Fraction)):
            msg = "a comma needs an integer prime and a rational ratio"
            raise TypeError(msg)
        if not is_prime(self.prime):
            msg = "a comma's target must be a prime"
            raise ValueError(msg)
        monzo = Monzo.of(self.ratio)
        if abs(monzo.exponent(self.prime)) != 1:
            msg = "a comma must hold its prime exactly once"
            raise NotationError(msg)
        object.__setattr__(self, "_monzo", monzo)


@dataclass(frozen=True, slots=True)
class Notation[N]:
    """連鎖と追加素数のコンマ規約からなる不変の記譜体系.

    ``chain`` は二素数の連鎖、``commas`` はそれぞれ独立した素数を追加する規約。
    型引数が同じでも、連鎖やコンマ規約が異なれば演算時に拒否する。
    """

    chain: ChainNotation
    commas: tuple[Comma, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.chain, ChainNotation):
            msg = "a notation needs a ChainNotation"
            raise TypeError(msg)
        commas = tuple(self.commas)
        if any(not isinstance(comma, Comma) for comma in commas):
            msg = "comma definitions must be Comma objects"
            raise TypeError(msg)
        if len({comma.prime for comma in commas}) != len(commas):
            msg = "two commas target the same prime"
            raise NotationError(msg)
        for comma in commas:
            prime = Monzo.of(comma.prime)
            rest = comma._monzo - prime * comma._monzo.exponent(comma.prime)
            if self.chain._locate(prime) is not None or self.chain._locate(rest) is None:
                msg = "a comma must extend the chain by exactly one independent prime"
                raise NotationError(msg)
        object.__setattr__(self, "commas", tuple(sorted(commas, key=lambda comma: comma.prime)))

    @property
    def primes(self) -> tuple[int, ...]:
        """連鎖とコンマ規約で綴れる素数を昇順で返す."""
        return tuple(sorted(self.chain._primes | {comma.prime for comma in self.commas}))

    def require(self, other: Notation[N]) -> None:
        """定義の値が一致しなければ拒否する."""
        if self != other:
            msg = "the notation definitions do not match"
            raise NotationError(msg)

    def interval(self, ratio: Fraction | int) -> Interval[N]:
        """正の有理比を綴り付き音程に変換する。体系で綴れない素数はNotationErrorで拒否する."""
        msg = "the ratio contains a prime this notation does not write"
        monzo = Monzo.over(ratio, self.primes)
        if monzo is None:
            raise NotationError(msg)
        rest = monzo
        counts = []
        for comma in self.commas:
            count = monzo.exponent(comma.prime) * comma._monzo.exponent(comma.prime)
            counts.append((comma.prime, count))
            rest -= comma._monzo * count
        chain = self.chain._locate(rest)
        if chain is None:
            raise NotationError(msg)
        return Interval(self, chain, tuple(counts))

    def _normalize(self, counts: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
        known = {comma.prime for comma in self.commas}
        total: dict[int, int] = {}
        for prime, count in counts:
            if type(prime) is not int or type(count) is not int:
                msg = "comma primes and counts must be integers"
                raise TypeError(msg)
            if prime not in known:
                msg = f"no comma writes {prime}"
                raise NotationError(msg)
            total[prime] = total.get(prime, 0) + count
        return tuple(sorted((prime, count) for prime, count in total.items() if count))

    def _monzo(self, chain: ChainInterval, counts: tuple[tuple[int, int], ...] = ()) -> Monzo:
        total = self.chain._monzo(chain)
        definitions = {comma.prime: comma._monzo for comma in self.commas}
        for prime, count in self._normalize(counts):
            total += definitions[prime] * count
        return total


@dataclass(frozen=True, slots=True)
class Interval[N]:
    """体系に結び付いた連鎖変位と、素数ごとのコンマ適用回数.

    ``chain`` は生成音程・周期の整数個数、``commas`` は ``(素数, 回数)`` の列。
    コンマの回数は同じ素数ごとに合算し、0となる成分を除く。
    加算は比の乗算、単項の負号は比の逆数に対応し、同じ記譜体系の音程同士で演算する。
    """

    notation: Notation[N]
    chain: ChainInterval
    commas: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.notation, Notation) or not isinstance(self.chain, ChainInterval):
            msg = "an interval needs a Notation and a chain Interval"
            raise TypeError(msg)
        if type(self.chain.generators) is not int or type(self.chain.periods) is not int:
            msg = "chain coordinates must be integers"
            raise TypeError(msg)
        object.__setattr__(self, "commas", self.notation._normalize(self.commas))

    @property
    def steps(self) -> int:
        """文字の幅を返す。同度は0で、下行する音程では負になる。コンマは数えない."""
        return self.notation.chain._steps(self.chain)

    @property
    def quality(self) -> Quality:
        """コンマを除いた綴りから、完全・長・短・増・減の性質を返す.

        性質は ``steps`` を一周期に収めた文字幅で決まる。文字が二つの体系では定まらず拒否する。
        """
        return self.notation.chain._quality(self.chain)

    def ratio(self) -> Fraction:
        """記譜上の正確な比を返す.

        生成音程・周期・コンマの比の積で、調律を適用する前の基準値である。
        音程列の上昇順もこの比で判定し、調律後の高さは ``cents`` で評価する。
        """
        return self._monzo().ratio()

    def cents(self, tuning: Tuning) -> float:
        """調律後の音程幅を返す."""
        return tuning.cents(self.ratio())

    def _monzo(self) -> Monzo:
        return self.notation._monzo(self.chain, self.commas)

    def __add__(self, other: Interval[N]) -> Self:
        """同じ記譜体系の音程を重ねた音程を返す。比の乗算に対応する."""
        if not isinstance(other, Interval):
            return NotImplemented
        self.notation.require(other.notation)
        return type(self)(self.notation, self.chain + other.chain, self.commas + other.commas)

    def __neg__(self) -> Self:
        """逆向きの音程を返す。比の逆数に対応する."""
        return type(self)(self.notation, -self.chain, tuple((prime, -count) for prime, count in self.commas))

    def __sub__(self, other: Interval[N]) -> Self:
        """``other`` を逆向きに重ねた音程を返す."""
        if not isinstance(other, Interval):
            return NotImplemented
        return self + (-other)
