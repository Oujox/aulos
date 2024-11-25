import typing as t

from .bases.base import BaseMT
from .setting import SettingMT
from .shared import HarmonicSystem


class ObjectMT(HarmonicSystem, BaseMT):

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is ObjectMT:
            raise TypeError("ObjectMT cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, setting: t.Optional[SettingMT] = None) -> None:
        if not isinstance(setting, SettingMT):
            raise ValueError(
                "Initialization error: 'setting' argument is missing. "
                "Please provide a valid setting object."
            )
        self._setting = setting
        super(ObjectMT, self).__init__(setting.semitone)

    @property
    def setting(self) -> SettingMT:
        return self._setting

    @property
    def scheme(self):
        return self._setting.scheme

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
