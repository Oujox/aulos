import typing as t
from abc import ABCMeta, abstractmethod

from .schema import Schema
from .setting import Setting
from .utils import classproperty


class AulosObject[T: Schema](metaclass=ABCMeta):
    """
    AulosObject is a base class for all objects in the Aulos library that require a schema and setting.

    This class provides a structured framework for objects that need to adhere to a
    specific schema and setting. It ensures that objects are instantiated with
    the correct schema and provides utility methods for schema and setting management.
    """

    _schema: T | None
    _setting: Setting | None

    def __new__(cls, *_args: t.Any, **_kwargs: t.Any) -> t.Self:
        if not hasattr(cls, "_schema"):
            msg = f"{cls.__name__} cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init__(self, setting: Setting | None = None) -> None:
        super().__init__()
        self._setting = setting

    def __init_subclass__(cls, *, schema: T | None = None) -> None:
        super().__init_subclass__()
        cls._schema = schema

    @classproperty
    def schema(self) -> T:
        """Returns the schema of the object."""
        if self._schema is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return self._schema

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
