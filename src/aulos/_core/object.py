import typing as t
from abc import ABCMeta

from .framework import InjectedMeta, OptimizedMeta
from .schema import Schema
from .setting import Setting


AulosObjectMeta = type("AulosObjectMeta", (InjectedMeta, OptimizedMeta, ABCMeta), {})


class AulosObject(metaclass=AulosObjectMeta):

    _setting: Setting
    _schema: Schema

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is AulosObject:
            raise TypeError("Object cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, setting: t.Optional[Setting] = None) -> None:
        if not isinstance(setting, Setting):
            raise ValueError(
                "Initialization error: 'setting' argument is missing. "
                "Please provide a valid setting object."
            )
        super(AulosObject, self).__init__()
        self._setting = setting
        self._schema = Schema(setting)

    @property
    def setting(self):
        return self._setting

    @property
    def schema(self):
        return self._schema

    def __eq__(self, other: t.Self) -> bool:
        return super(object, self).__eq__(other)

    def __ne__(self, other: t.Self) -> bool:
        return super(object, self).__ne__(other)

    def __str__(self) -> str:
        return "<Object: semitone={}, setting={}>".format(
            self.schema.semitone, self._setting
        )

    def __repr__(self) -> str:
        return "<Object: semitone={}, setting={}>".format(
            self.schema.semitone, self._setting
        )
