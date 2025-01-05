from abc import abstractmethod


class BasePitchClass:
    __slots__ = ()

    @abstractmethod
    def __int__(self) -> int: ...

    @property
    @abstractmethod
    def pitchclass(self) -> int: ...

    @property
    @abstractmethod
    def pitchname(self) -> str | None: ...

    @property
    @abstractmethod
    def pitchnames(self) -> list[str]: ...
