import typing as t
from abc import ABCMeta, abstractmethod
from typing import cast

from .schema import Schema
from .setting import Setting
from .utils import classproperty


class AulosObject(metaclass=ABCMeta):
    """
    AulosObject is the base class for all objects in the Aulos framework.
    It provides a common interface and structure for all objects, including methods for equality checks,
    """

    _setting: Setting | None

    def __init__(self, setting: Setting | None = None) -> None:
        super().__init__()
        self._setting = setting

    @property
    def setting(self) -> Setting | None:
        """Returns the setting of the object."""
        return self._setting

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...

    @abstractmethod
    def __ne__(self, other: object) -> bool: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...


class AulosSchemaObject[S: Schema](AulosObject):
    """
    AulosSchemaObject is a base class for objects that are associated with a schema.
    It provides a common interface for schema validation and access to the schema.
    """

    _schema: t.ClassVar[Schema | None]

    def __init_subclass__(cls, *, schema: S | None = None) -> None:
        super().__init_subclass__()
        cls._schema = schema

    @classproperty
    def schema(self) -> S:
        if self._schema is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return cast("S", self._schema)
