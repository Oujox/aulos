"""綴りと音名の変換規約。記号はすべて外部から指定する."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from aulos.core.chain import Spelling
from aulos.core.errors import RepresentationError
from aulos.core.monzo import Monzo

if TYPE_CHECKING:
    from aulos.core.notation import Notation

type _Commas = tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class CommaSymbols:
    """素数のコンマ数を表示する正方向・負方向の記号."""

    prime: int
    raised: str
    lowered: str

    def __post_init__(self) -> None:
        if type(self.prime) is not int:
            msg = "comma symbol targets must be integer primes"
            raise TypeError(msg)
        if not isinstance(self.raised, str) or not isinstance(self.lowered, str):
            msg = "comma marks must be strings"
            raise TypeError(msg)
        if self.prime < 2 or Monzo.of(self.prime).exponents != ((self.prime, 1),):  # noqa: PLR2004
            msg = "comma symbol targets must be primes"
            raise ValueError(msg)
        if any(not mark or any(char.isdigit() or char == "-" for char in mark) for mark in (self.raised, self.lowered)):
            msg = "comma marks must be nonempty and contain no register characters"
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Symbols:
    """音名の表示記号.

    ``letters`` は原点の文字から高さ順に並べ、変化記号は最大 ``most`` 個まで記す。
    音域番号は文字 ``turn`` で進み、原点と同じ内部音域にある ``turn`` の番号を ``label`` とする。
    七文字がFから始まりCで番号が進むなら ``turn=4``、``label=4`` で F3 G3 A3 B3 C4 となる。
    """

    letters: tuple[str, ...]
    raised: str
    lowered: str
    most: int
    turn: int
    label: int
    commas: tuple[CommaSymbols, ...] = ()

    def __post_init__(self) -> None:
        if any(type(value) is not int for value in (self.most, self.turn, self.label)):
            msg = "most, turn, and label must be integers"
            raise TypeError(msg)
        self._freeze_symbols()
        symbols = [*self.letters, self.raised, self.lowered]
        if any(symbol == "" for symbol in symbols):
            msg = "a symbol is empty"
            raise ValueError(msg)
        self._validate_marks(symbols)
        if not 0 <= self.turn < len(self.letters):
            msg = f"labels cannot advance at letter {self.turn}: there are {len(self.letters)}"
            raise ValueError(msg)
        if self.most < 0:
            msg = f"at most {self.most} alterations"
            raise ValueError(msg)

    def _freeze_symbols(self) -> None:
        object.__setattr__(self, "letters", tuple(self.letters))
        object.__setattr__(self, "commas", tuple(self.commas))
        if any(not isinstance(comma, CommaSymbols) for comma in self.commas):
            msg = "comma symbols must be CommaSymbols objects"
            raise TypeError(msg)
        if len({comma.prime for comma in self.commas}) != len(self.commas):
            msg = "comma symbol targets must be unique"
            raise ValueError(msg)

    def _validate_marks(self, symbols: list[str]) -> None:
        if len(set(self.letters)) != len(self.letters):
            msg = "two letters share a symbol"
            raise ValueError(msg)
        marks = [*symbols, *(mark for comma in self.commas for mark in (comma.raised, comma.lowered))]
        for index, mark in enumerate(marks):
            for other in marks[index + 1 :]:
                if mark.startswith(other) or other.startswith(mark):
                    msg = f"the symbols {mark!r} and {other!r} could be read in each other's place"
                    raise ValueError(msg)
            if any(char.isdigit() or char == "-" for char in mark):
                msg = f"the symbol {mark!r} holds a register label's characters"
                raise ValueError(msg)

    def validate(self, notation: Notation) -> None:
        """文字数と必要なコンマ記号が記譜体系に対応するか検証する."""
        if len(self.letters) != notation.chain.size:
            msg = "the symbol letters do not match the notation"
            raise RepresentationError(msg)
        if {comma.prime for comma in notation.commas} - {comma.prime for comma in self.commas}:
            msg = "the notation needs comma symbols"
            raise RepresentationError(msg)

    def _render_name(self, letter: int, alteration: int) -> str:
        if not 0 <= letter < len(self.letters):
            msg = f"letter {letter} has no symbol"
            raise RepresentationError(msg)
        if abs(alteration) > self.most:
            msg = f"{alteration} alterations: at most {self.most} are written"
            raise RepresentationError(msg)
        mark = self.raised if alteration > 0 else self.lowered
        return self.letters[letter] + mark * abs(alteration)

    def _render(self, spelling: Spelling) -> str:
        name = self._render_name(spelling.letter, spelling.alteration)
        return f"{name}{spelling.register + self.label - (spelling.letter < self.turn)}"

    def _read_name(self, text: str) -> tuple[int, int, str] | None:
        """先頭の文字と変化記号を読み、文字位置・変化量・残りを返す。文字で始まらなければNone."""
        letter = next((index for index, symbol in enumerate(self.letters) if text.startswith(symbol)), None)
        if letter is None:
            return None
        rest = text[len(self.letters[letter]) :]
        alteration = 0
        for mark, sign in ((self.raised, 1), (self.lowered, -1)):
            while rest.startswith(mark):
                rest = rest[len(mark) :]
                alteration += sign
            if alteration:
                break
        if abs(alteration) > self.most:
            msg = f"{text!r} is not a name of this notation"
            raise ValueError(msg)
        return letter, alteration, rest

    def _register(self, letter: int, label: int) -> int:
        """表示上の番号を内部音域にする。``turn`` より前の文字は表示番号が一つ小さい."""
        return label - self.label + (letter < self.turn)

    def _parse(self, name: str) -> Spelling:
        read = self._read_name(name)
        if read is None:
            msg = f"{name!r} does not start with a letter"
            raise ValueError(msg)
        letter, alteration, rest = read
        try:
            label = int(rest)
        except ValueError:
            msg = f"{name!r} does not end with a register"
            raise ValueError(msg) from None
        if str(label) != rest:
            msg = f"{name!r} is not a name of this notation"
            raise ValueError(msg)
        return Spelling(letter, alteration, self._register(letter, label))

    def _render_commas(self, counts: _Commas) -> str:
        marks = {comma.prime: comma for comma in self.commas}
        result = []
        for prime, count in counts:
            if prime not in marks:
                msg = f"no symbol writes comma {prime}"
                raise RepresentationError(msg)
            symbols = marks[prime]
            result.append((symbols.raised if count > 0 else symbols.lowered) * abs(count))
        return "".join(result)

    def _render_pitch(self, spelling: Spelling, commas: _Commas) -> str:
        return self._render(spelling) + self._render_commas(commas)

    def _render_class(self, letter: int, alteration: int, commas: _Commas) -> str:
        return self._render_name(letter, alteration) + self._render_commas(commas)

    def _read_commas(self, text: str) -> tuple[_Commas, str]:
        """先頭のコンマ記号を読み、素数ごとの回数の列と残りを返す."""
        counts = []
        while True:
            found = next(
                (
                    (comma.prime, sign, mark)
                    for comma in self.commas
                    for sign, mark in ((1, comma.raised), (-1, comma.lowered))
                    if text.startswith(mark)
                ),
                None,
            )
            if found is None:
                return tuple(counts), text
            prime, sign, mark = found
            counts.append((prime, sign))
            text = text[len(mark) :]

    def _parse_pitch(self, name: str) -> tuple[Spelling, _Commas]:
        """音域付きの音名を綴りとコンマ数にする."""
        match = re.fullmatch(r"(.+?-?\d+)(.*)", name, re.DOTALL)
        if match is None:
            msg = "a pitch name needs a register"
            raise ValueError(msg)
        base, suffix = match.groups()
        spelling = self._parse(base)
        commas, rest = self._read_commas(suffix)
        if rest:
            msg = "unknown comma symbol"
            raise ValueError(msg)
        return spelling, commas

    def _split_root(self, text: str) -> tuple[Spelling, _Commas, str]:
        """先頭の音域なし音名とコンマ記号を読む。音域は基準の番号にある位置とする."""
        read = self._read_name(text)
        if read is None:
            msg = "a symbol must start with a root letter"
            raise ValueError(msg)
        letter, alteration, rest = read
        commas, rest = self._read_commas(rest)
        return Spelling(letter, alteration, self._register(letter, self.label)), commas, rest

    def _parse_class(self, name: str) -> tuple[int, int, _Commas]:
        """音域なしの音名を文字位置・変化量・コンマ数にする."""
        spelling, commas, rest = self._split_root(name)
        if rest:
            msg = "unexpected text after the pitch class"
            raise ValueError(msg)
        return spelling.letter, spelling.alteration, commas
