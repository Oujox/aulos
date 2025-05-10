from abc import ABCMeta, abstractmethod


class Schema(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the schema. This method should be implemented by subclasses to perform
        any necessary validation checks on the schema.
        """
        msg = "Subclasses must implement the validate method."
        raise NotImplementedError(msg)
