from abc import abstractmethod


class BaseTuner:

    @abstractmethod
    def hz(self, note_number: int) -> float: ...
