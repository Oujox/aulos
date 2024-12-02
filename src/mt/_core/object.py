import typing as t

from .bases.base import Base
from .coexistence import Coexistence
from .schema import Schema
from .setting import Setting


class Object(Coexistence, Base):

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Object:
            raise TypeError("ObjectMT cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, setting: t.Optional[Setting] = None) -> None:
        if not isinstance(setting, Setting):
            raise ValueError(
                "Initialization error: 'setting' argument is missing. "
                "Please provide a valid setting object."
            )
        self._setting = setting
        self._scheme = Schema(setting)
        super(Object, self).__init__(setting.pitchclass.semitone)

    @property
    def setting(self):
        return self._setting

    @property
    def scheme(self):
        return self._scheme

    def __eq__(self, other: t.Self) -> bool:
        return super(object, self).__eq__(other)

    def __ne__(self, other: t.Self) -> bool:
        return super(object, self).__ne__(other)

    def __str__(self) -> str:
        return "<ObjectMT: semitone={}, setting={}>".format(
            self.semitone, self._setting
        )

    def __repr__(self) -> str:
        return "<ObjectMT: semitone={}, setting={}>".format(
            self.semitone, self._setting
        )
