import tkinter as tk
import typing as t
from tkinter import ttk

from aulos.TET12 import scale
from aulos.ui.components.base import BaseComponent
from aulos.ui.services import ScaleService


class ScaleSelecter(BaseComponent):
    _selected_scalename: tk.StringVar
    _selected_scaleinfo: tk.StringVar

    _wrap: ttk.Frame
    _title: ttk.Label
    _scalegroups: tuple[ttk.Frame, ttk.Frame]
    _scalebuttons: tuple[list[ttk.Radiobutton], list[ttk.Radiobutton]]

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master
        self.service = ScaleService()
        self.bind_callback("on_click_scalebutton", self.update_scaleinfo)

    def create_widget(self) -> None:
        self._selected_scalename = tk.StringVar()
        self._selected_scaleinfo = tk.StringVar()

        self._wrap = ttk.Frame(
            self,
            padding=(24, 8),
            borderwidth=2,
            relief=tk.SOLID,
        )
        self._title = ttk.Label(self, text="Scale")
        self._wrap.pack()
        self._title.place(relx=0.05, rely=0, anchor=tk.W)

        self._scalegroups = (
            ttk.Frame(self._wrap, padding=(6, 0)),
            ttk.Frame(self._wrap, padding=(6, 0)),
        )
        self._scalebuttons = (
            [
                ttk.Radiobutton(
                    self._scalegroups[0],
                    text=scale,
                    value=scale,
                    variable=self._selected_scalename,
                    command=self.trigger_event("on_click_scalebutton"),
                )
                for scale in self.service.get_tonalscalenames()
            ],
            [
                ttk.Radiobutton(
                    self._scalegroups[1],
                    text=mode,
                    value=mode,
                    variable=self._selected_scalename,
                    command=self.trigger_event("on_click_scalebutton"),
                )
                for mode in self.service.get_modalscalenames()
            ],
        )

        for scalegroup in self._scalegroups:
            scalegroup.pack(side=tk.LEFT, anchor=tk.NW)

        for scalebuttons in self._scalebuttons:
            for btn in scalebuttons:
                btn.pack(side=tk.TOP, anchor=tk.NW)

    def default(self) -> None:
        self._selected_scalename.set(scale.Major.__name__)
        self._selected_scaleinfo.set(scale.Major.__doc__ or "")

    def set_callback_on_click_scalebutton(self, callback: t.Callable[[], t.Any]) -> None:
        self.bind_callback("on_click_scalebutton", callback)

    def update_scaleinfo(self) -> None:
        scalename = self._selected_scalename.get()
        scale = self.service.get_scale(scalename)
        self._selected_scaleinfo.set(scale.__doc__ or "")

    @property
    def scalename(self) -> str:
        return self._selected_scalename.get()

    @property
    def scaleinfo(self) -> str:
        return self._selected_scaleinfo.get()
