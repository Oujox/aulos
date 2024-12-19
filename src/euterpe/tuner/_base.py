from abc import abstractmethod


class BaseTuner:
    __slots__ = ()

    @abstractmethod
    def hz(self, notenumber: int) -> float: ...
