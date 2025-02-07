import typing as t

from aulos._core.utils import OptimizedMeta

from .schema import Schema
from .setting import Setting
from .utils import classproperty


class AulosObjectMeta(OptimizedMeta):
    """
    AulosObjectMeta is a metaclass that enforces a schema and optional settings.

    This metaclass is designed to ensure that any class using it adheres to a specific schema,
    which is a structured representation of the class's data and behavior. It also allows for
    optional settings that can be customized for each subclass. The metaclass provides mechanisms
    to validate and initialize these schemas and settings, ensuring consistency and correctness
    across all instances of the class.
    """


class AulosObject[T: Schema](metaclass=AulosObjectMeta):
    """
    AulosObject is a base class for all objects in the Aulos library that require a schema and setting.

    This class provides a structured framework for objects that need to adhere to a
    specific schema and setting. It ensures that objects are instantiated with
    the correct schema and provides utility methods for schema and setting management.
    """

    _schema: T
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
        return self._schema

    @property
    def setting(self) -> Setting | None:
        """Returns the setting of the object."""
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
