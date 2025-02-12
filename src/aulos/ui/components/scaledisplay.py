import tkinter as tk
import typing as t
from tkinter import ttk

from .base import BaseComponent


class ScaleDisplay(BaseComponent):
    _scale: tk.StringVar
    _keyname: tk.StringVar
    _scalename: tk.StringVar
    _scaleinfo: tk.StringVar

    _wrapper: ttk.Frame
    _scaledisplay: ttk.Label
    _scaleinfodisplay: ttk.Label

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master

    def create_widget(self) -> None:
        self._scale = tk.StringVar()
        self._keyname = tk.StringVar()
        self._scalename = tk.StringVar()
        self._scaleinfo = tk.StringVar()

        def combine(*_args: t.Any) -> None:
            self._scale.set(f"{self.keyname} {self.scalename}")

        self._keyname.trace_add("write", combine)
        self._scalename.trace_add("write", combine)

        self._wrapper = ttk.Frame(self, padding=(24, 8), borderwidth=2, relief=tk.SOLID)
        self._scaledisplay = ttk.Label(
            self._wrapper,
            textvariable=self._scale,
            font=("Times", 18),
        )
        self._scaleinfodisplay = ttk.Label(
            self._wrapper,
            textvariable=self._scaleinfo,
            font=("Times", 10),
        )

        self._wrapper.pack()
        self._scaledisplay.pack(side=tk.TOP, anchor=tk.NW)
        self._scaleinfodisplay.pack(side=tk.TOP, anchor=tk.NW)

    def default(self) -> None:
        return

    @property
    def keyname(self) -> str:
        return self._keyname.get()

    @keyname.setter
    def keyname(self, value: str) -> None:
        return self._keyname.set(value)

    @property
    def scalename(self) -> str:
        return self._scalename.get()

    @scalename.setter
    def scalename(self, value: str) -> None:
        self._scalename.set(value)

    @property
    def scaleinfo(self) -> str:
        return self._scaleinfo.get()

    @scaleinfo.setter
    def scaleinfo(self, value: str) -> None:
        self._scaleinfo.set(value)
