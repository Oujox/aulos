import typing as t

from .schema import Schema
from .setting import Setting
from .utils import classproperty


class AulosObject[T: Schema]:
    """
    AulosObject is a generic base class that enforces a schema and optional settings.

    Type Parameters:
        T (Schema): The schema type that the class will enforce.

    Attributes:
        _schema (T): The schema associated with the object.
        _setting (Setting | None): Optional settings for the object.
    """

    _schema: T
    _setting: Setting | None

    __slots__ = ("_setting",)

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
