import typing as t
from abc import ABCMeta

from .framework import InjectedMeta, OptimizedMeta
from .schema import Schema
from .setting import Setting
from .utils import classproperty

AulosObjectMeta = type("AulosObjectMeta", (InjectedMeta, OptimizedMeta, ABCMeta), {})


class AulosObject[T: Schema](metaclass=AulosObjectMeta):
    _schema: T
    _setting: Setting | None

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is AulosObject:
            raise TypeError("AulosObject cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, setting: Setting | None = None) -> None:
        super(AulosObject, self).__init__()
        self._setting = setting

    def __init_subclass__(cls, *, schema: T | None = None) -> None:
        if schema is None:
            return
        super(AulosObject, cls).__init_subclass__()
        cls._schema = schema

    @classproperty
    def schema(cls) -> T:
        return cls._schema

    @property
    def setting(self) -> Setting | None:
        return self._setting

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, AulosObject):
            return NotImplemented
        return self._schema == self._schema and self._setting == other._setting

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<AulosObject: setting={}>".format(self._setting)

    def __repr__(self) -> str:
        return "<AulosObject: setting={}>".format(self._setting)
