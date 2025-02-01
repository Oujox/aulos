import typing as t
from abc import ABCMeta

from .framework import InjectedMeta, OptimizedMeta
from .schema import Schema
from .setting import Setting
from .utils import classproperty


class AulosObjectMeta(InjectedMeta, OptimizedMeta, ABCMeta):
    """This metaclass enables dependency injection, optimizations, and abstract base class capabilities."""


class AulosObject[T: Schema, *_](metaclass=AulosObjectMeta):
    _schema: T
    _setting: Setting | None

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is AulosObject:
            msg = "AulosObject cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init__(self, setting: Setting | None = None) -> None:
        super().__init__()
        self._setting = setting

    def __init_subclass__(cls, *, schema: T | None = None) -> None:
        if schema is None:
            return
        super().__init_subclass__()
        cls._schema = schema

    @classproperty
    def schema(self) -> T:
        return self._schema

    @property
    def setting(self) -> Setting | None:
        return self._setting

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AulosObject):
            return NotImplemented
        return self._schema == self._schema and self._setting == other._setting

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<AulosObject: setting={self._setting}>"

    def __repr__(self) -> str:
        return f"<AulosObject: setting={self._setting}>"
