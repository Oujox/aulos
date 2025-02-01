import tkinter as tk
import typing as t
from abc import ABCMeta, abstractmethod


class BaseComponent(tk.Frame, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc, **kwargs: t.Any) -> None:
        super().__init__(master, padx=12, pady=4, **kwargs)

    @abstractmethod
    def create_widget(self, *args: t.Any, **kwargs: t.Any) -> None: ...

    @abstractmethod
    def default(self) -> None: ...
