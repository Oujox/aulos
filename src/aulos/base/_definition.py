"""分類の方針と、体系をクラス属性に束ねる基底."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from inspect import isabstract
from typing import ClassVar

from aulos.core.errors import TemperamentError
from aulos.core.notation import Notation
from aulos.core.symbols import Symbols
from aulos.core.temper import Tuning


class Tag[Spec](ABC):
    """定義が分類の条件を満たすか検証する方針."""

    @classmethod
    @abstractmethod
    def validate(cls, spec: Spec) -> None:
        """分類に適合しない定義を拒否する."""


class NotationTag(Tag[Notation], ABC):
    """記譜体系の分類。同じTagでも定義の一致は保証しない."""


class Definition[N: NotationTag]:
    """体系をクラス属性に束ねる基底。具体クラスの定義は作成時に検証する."""

    notation: Notation[N]
    symbols: ClassVar[Symbols]
    tag: type[N]
    tuning: ClassVar[Tuning | None] = None
    is_abstract: ClassVar[bool] = True

    def __init_subclass__(cls, *, abstract: bool = False, **kwargs: object) -> None:
        """``abstract=True`` の中間クラスは検証を省略する."""
        super().__init_subclass__(**kwargs)
        cls.is_abstract = abstract or isabstract(cls)
        if not cls.is_abstract:
            cls.validate_definition()

    @classmethod
    def validate_definition(cls) -> None:
        """束ねた定義の型と相互の整合性を検証する."""
        cls._validate_instance("notation", Notation)
        cls._validate_instance("symbols", Symbols)
        tag = getattr(cls, "tag", None)
        if not isinstance(tag, type) or not issubclass(tag, NotationTag) or isabstract(tag):
            msg = "tag must be a concrete NotationTag subclass"
            raise TypeError(msg)
        tag.validate(cls.notation)
        cls.symbols.validate(cls.notation)
        if cls.tuning is not None:
            cls._validate_instance("tuning", Tuning)
            chain = cls.notation.chain
            for ratio in (chain.generator, *(comma.ratio for comma in cls.notation.commas)):
                cls.tuning.cents(ratio)
            # 周期が上行しない調律では、音域を上げても音が高くならない。
            if cls.tuning.cents(chain.period) <= 0:
                msg = "the bound tuning must give the period a positive size"
                raise TemperamentError(msg)

    @classmethod
    def _validate_instance(cls, attribute: str, expected: type) -> None:
        if not isinstance(getattr(cls, attribute, None), expected):
            msg = f"{cls.__name__}.{attribute} must be a {expected.__name__}"
            raise TypeError(msg)

    @classmethod
    def _validate_type(cls, attribute: str, expected: type[Definition]) -> None:
        value = getattr(cls, attribute, None)
        if not isinstance(value, type) or not issubclass(value, expected) or value.is_abstract:
            msg = f"{attribute} must be a concrete {expected.__name__} subclass"
            raise TypeError(msg)
        cls.notation.require(value.notation)

    @classmethod
    def _require_concrete(cls) -> None:
        if cls.is_abstract:
            msg = "an abstract definition cannot be instantiated"
            raise TypeError(msg)

    @classmethod
    def _resolve_tuning(cls, tuning: Tuning | None) -> Tuning:
        resolved = cls.tuning if tuning is None else tuning
        if resolved is None:
            msg = "a tuning is required: this definition binds none"
            raise TypeError(msg)
        return resolved


def require_symbol(symbol: str) -> None:
    """音名やテンプレート名の入口が文字列であることを検証する."""
    if not isinstance(symbol, str):
        msg = "a symbol must be a string"
        raise TypeError(msg)
