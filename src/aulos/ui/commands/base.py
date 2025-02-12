import argparse as ap
import typing as t
from abc import ABCMeta, abstractmethod


class BaseCLI(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, parser: ap.ArgumentParser, **kwargs: t.Any) -> None:
        parser.set_defaults(execute=self.execute)

    @abstractmethod
    def execute(self, args: ap.Namespace) -> None:
        return
