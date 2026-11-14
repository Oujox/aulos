"""素因数の指数ベクトルの線形写像としての調律.

写像の各行が生成音程、各列が素数に対応する。ゼロに写る比は調律で消失し、
その比だけ異なる綴りが同音になる。音程幅は ``Tuning`` が与えて初めて決まる。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from typing import TYPE_CHECKING

from aulos.core.chain import Spelling
from aulos.core.errors import TemperamentError
from aulos.core.maths import Matrix
from aulos.core.maths import cents_of
from aulos.core.maths import float_dot
from aulos.core.maths import is_prime
from aulos.core.maths import round_half_up
from aulos.core.maths import scale_by_cents
from aulos.core.maths import sizes_in_period
from aulos.core.monzo import Monzo

if TYPE_CHECKING:
    from aulos.core.chain import ChainNotation
    from aulos.core.chain import ChainPitch

_RESOLVABLE = 2**53
"""これ以上の位置ではfloatが隣の整数を区別できない."""


@dataclass(frozen=True, slots=True)
class Temperament:
    """素数の指数を生成音程の個数に写す整数行列.

    ``primes`` の順序が行列の列に対応し、``rows`` の各行が生成音程に対応する。
    生成音程の幅は持たず、セント値への評価には ``Tuning`` が必要。
    """

    primes: tuple[int, ...]
    rows: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "primes", tuple(self.primes))
        object.__setattr__(self, "rows", tuple(tuple(row) for row in self.rows))
        if any(not isinstance(prime, int) for prime in self.primes):
            msg = "prime basis entries must be integers"
            raise TypeError(msg)
        if not self.primes or len(set(self.primes)) != len(self.primes) or not all(map(is_prime, self.primes)):
            msg = "a temperament needs distinct primes"
            raise ValueError(msg)
        if any(not isinstance(value, int) for row in self.rows for value in row):
            msg = "temperament matrix entries must be integers"
            raise TypeError(msg)
        if not self.rows or any(len(row) != len(self.primes) for row in self.rows):
            msg = "a temperament needs rows of one count per prime"
            raise ValueError(msg)

    @property
    def rank(self) -> int:
        """行数を返す。行列の数学的な階数ではない."""
        return len(self.rows)

    @property
    def _matrix(self) -> Matrix:
        """素数の指数ベクトルを生成音程の個数に写す行列."""
        return Matrix(self.rows)

    @classmethod
    def equal_division(cls, primes: tuple[int, ...], divisions: int, period: Fraction) -> Temperament:
        """周期を等分し、各素数を最寄りのステップに写す写像を返す.

        周期がちょうど ``divisions`` に写らない組み合わせ(平方の周期を奇数等分するなど)と、
        最寄りのステップを浮動小数点で決められない規模は拒否する。
        """
        if not isinstance(divisions, int):
            msg = "divisions must be an integer"
            raise TypeError(msg)
        if divisions <= 0 or period <= 1:
            msg = "divisions must be positive and period must be above 1"
            raise ValueError(msg)
        # 対数を取る前に基底を検証し、標準の値域エラーと体系の不正を混同しない。
        cls(primes, (tuple(0 for _ in primes),))
        period = Fraction(period)
        sizes = sizes_in_period(primes, period)
        if divisions >= _RESOLVABLE or divisions * max(sizes) >= _RESOLVABLE:
            msg = f"{divisions} divisions are too fine to find the nearest steps"
            raise TemperamentError(msg)
        division = cls(primes, (tuple(round_half_up(divisions * size) for size in sizes),))
        if division.map(period) != (divisions,):
            msg = f"the nearest steps do not divide the period {period} into {divisions}"
            raise TemperamentError(msg)
        return division

    def map(self, ratio: Fraction | int) -> tuple[int, ...]:
        """比を各生成音程の個数に写す."""
        monzo = Monzo.over(ratio, self.primes)
        if monzo is None:
            msg = "the ratio has primes that are not mapped"
            raise TemperamentError(msg)
        return (self._matrix @ monzo.vector(self.primes)).entries

    def tempers_out(self, ratio: Fraction | int) -> bool:
        """比がゼロに写るか判定する。該当する比の両端は同音になる."""
        return not any(self.map(ratio))

    def letter_steps(self, chain: ChainNotation) -> tuple[tuple[int, ...], int]:
        """隣接する文字間と変化音程のステップ数を返す。出力が1成分の写像のみ対応する."""
        if self.rank != 1:
            msg = "letter steps need a temperament with a single generator"
            raise TemperamentError(msg)
        letters = [chain._pitch(Spelling(letter, 0, 0)) for letter in range(chain.size)]
        letters.append(chain._pitch(Spelling(0, 0, 1)))
        heights = [self.map(chain._ratio(pitch))[0] for pitch in letters]
        alteration = self.map(chain._ratio(chain.alteration))[0]
        return tuple(high - low for low, high in pairwise(heights)), alteration

    def _spellings(self, chain: ChainNotation, step: int, most: int) -> tuple[ChainPitch, ...]:
        """``step`` に対応する変化量 ``most`` 以下の音高を、変化量の絶対値・文字の順で返す."""
        if most < 0:
            msg = "the alteration limit must not be negative"
            raise ValueError(msg)
        between, alteration = self.letter_steps(chain)
        if alteration <= 0 or any(size <= 0 for size in between):
            msg = f"the letters do not rise by these steps: {between}, an alteration {alteration}"
            raise TemperamentError(msg)
        period = sum(between)
        found = []
        for letter in range(chain.size):
            natural = self.map(chain._ratio(chain._pitch(Spelling(letter, 0, 0))))[0]
            for altered in range(-most, most + 1):
                register, rest = divmod(step - natural - altered * alteration, period)
                if not rest:
                    found.append(chain._pitch(Spelling(letter, altered, register)))
        spelled = {pitch: chain._spell(pitch) for pitch in found}
        return tuple(sorted(found, key=lambda pitch: (abs(spelled[pitch].alteration), spelled[pitch].letter)))


@dataclass(frozen=True, slots=True)
class Tuning:
    """調律写像の各生成音程に、セント単位の音程幅を与える.

    ``temperament`` は整数行列の写像、``sizes`` は各行に対応する有限のセント値。
    ``cents`` と ``frequency`` はこの幅を使って音程比を評価する。
    """

    temperament: Temperament
    sizes: tuple[float, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "sizes", tuple(self.sizes))
        if len(self.sizes) != self.temperament.rank or not all(math.isfinite(size) for size in self.sizes):
            msg = "a tuning needs a finite size for each generator"
            raise ValueError(msg)

    @classmethod
    def just(cls, primes: tuple[int, ...]) -> Tuning:
        """各素数を純正な幅のまま保つ調律を返す."""
        rows = tuple(tuple(int(row == column) for column in range(len(primes))) for row in range(len(primes)))
        temperament = Temperament(primes, rows)
        return cls(temperament, tuple(cents_of(prime) for prime in temperament.primes))

    def cents(self, ratio: Fraction | int) -> float:
        """調律後の音程幅をセント単位で返す。floatで表せない幅は拒否する."""
        cents = float_dot(self.temperament.map(ratio), self.sizes)
        if not math.isfinite(cents):
            msg = "the tuned interval is outside the range of a float"
            raise ValueError(msg)
        return cents

    def frequency(self, ratio: Fraction | int, anchor_hz: float) -> float:
        """正の有限な基準周波数 ``anchor_hz`` から ``ratio`` だけ離れた周波数をHzで返す.

        指数を合成してから評価するため、結果が表現できる限り途中であふれない。
        表現できない結果は拒否する。
        """
        if not math.isfinite(anchor_hz) or anchor_hz <= 0:
            msg = "frequency needs a positive finite anchor"
            raise ValueError(msg)
        result = scale_by_cents(anchor_hz, self.cents(ratio))
        if result == 0 or math.isinf(result):
            msg = "the frequency is outside the range of a float"
            raise ValueError(msg)
        return result
