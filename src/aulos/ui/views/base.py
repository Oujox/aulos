import argparse as ap
import tkinter as tk
import typing as t
from abc import ABCMeta, abstractmethod


class BaseGUI(tk.Frame, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc, **kwargs: t.Any) -> None:
        super().__init__(master, **kwargs)

    @abstractmethod
    def create_widget(self, *args: t.Any, **kwargs: t.Any) -> None:
        return

    @abstractmethod
    def default(self) -> None:
        return


class BaseCLI(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, parser: ap.ArgumentParser, **kwargs: t.Any) -> None:
        parser.set_defaults(execute=self.execute)

    @abstractmethod
    def execute(self, args: ap.Namespace) -> None:
        return
