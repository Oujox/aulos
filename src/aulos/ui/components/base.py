import tkinter as tk
from abc import ABCMeta, abstractmethod


class BaseComponent(tk.Frame, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc, **kwargs) -> None:
        super().__init__(master, padx=12, pady=4, **kwargs)

    @abstractmethod
    def create_widget(self, *args, **kwargs) -> None: ...

    @abstractmethod
    def default(self) -> None: ...
