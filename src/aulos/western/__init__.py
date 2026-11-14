"""西洋式七文字記譜の共通定義。具体クラスは ``equal`` と ``just`` にある."""

from fractions import Fraction

from aulos.base import ChainNotation
from aulos.base import Notation
from aulos.base import NotationError
from aulos.base import NotationTag

chain = ChainNotation(Fraction(2), Fraction(3, 2), 7)
letters = ("F", "G", "A", "B", "C", "D", "E")


class WesternTag(NotationTag):
    """完全5度とオクターブによる七文字の分類。コンマ規約は限定しない."""

    @classmethod
    def validate(cls, spec: Notation) -> None:
        """西洋式の文字配置を持つことを検証する."""
        if spec.chain != chain:
            msg = "western notation needs the seven-letter fifth chain"
            raise NotationError(msg)


__all__ = ["WesternTag", "chain", "letters"]
