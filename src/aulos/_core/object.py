import typing as t

from .bases.base import Base
from .coexistence import Coexistence
from .logic import Logic
from .setting import Setting


class AulosObject(Coexistence, Base):

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
        super(AulosObject, self).__init__(intervals=setting.pitchclass.intervals)
        self._setting = setting
        self._logic = Logic(setting)

    @property
    def setting(self):
        return self._setting

    @property
    def logic(self):
        return self._logic

    def __eq__(self, other: t.Self) -> bool:
        return super(object, self).__eq__(other)

    def __ne__(self, other: t.Self) -> bool:
        return super(object, self).__ne__(other)

    def __str__(self) -> str:
        return "<Object: semitone={}, setting={}>".format(
            self.logic.semitone, self._setting
        )

    def __repr__(self) -> str:
        return "<Object: semitone={}, setting={}>".format(
            self.logic.semitone, self._setting
        )
