import typing as t
from abc import ABCMeta

from .framework import InjectedMeta, OptimizedMeta
from .schema import Schema
from .setting import Setting

EuterpeObjectMeta = type(
    "EuterpeObjectMeta", (InjectedMeta, OptimizedMeta, ABCMeta), {}
)


class EuterpeObject(metaclass=EuterpeObjectMeta):

    _setting: Setting
    _schema: Schema

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is EuterpeObject:
            raise TypeError("Object cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, setting: t.Optional[Setting] = None) -> None:
        if not isinstance(setting, Setting):
            raise ValueError(
                "Initialization error: 'setting' argument is missing. "
                "Please provide a valid setting object."
            )
        super(EuterpeObject, self).__init__()
        self._setting = setting
        self._schema = Schema(setting)

    @property
    def setting(self):
        return self._setting

    @property
    def schema(self):
        return self._schema
