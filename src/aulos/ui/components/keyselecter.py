import tkinter as tk
import typing as t
from tkinter import ttk

from aulos.ui.components.base import BaseComponent

KEY_DEFAULTS = (
    ("Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"),
    ("C", "D", "E", "F", "G", "A", "B"),
    ("C#", "D#", "E#", "F#", "G#", "A#", "B#"),
)


class KeySelecter(BaseComponent):
    selected_keyname: tk.StringVar

    _wrap: ttk.Frame
    _title: ttk.Label
    _keygroups: list[ttk.Frame]
    _keybuttons: list[list[ttk.Radiobutton]]

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master

    def create_widget(self) -> None:
        self.selected_keyname = tk.StringVar()
        self._wrap = ttk.Frame(
            self,
            padding=(24, 8),
            borderwidth=2,
            relief=tk.SOLID,
        )
        self._title = ttk.Label(self, text="Key")
        self._wrap.pack()
        self._title.place(relx=0.05, rely=0, anchor=tk.W)

        self._keygroups = [ttk.Frame(self._wrap, padding=(6, 0)) for _ in range(len(KEY_DEFAULTS))]
        self._keybuttons = [
            [
                ttk.Radiobutton(
                    keygroup,
                    text=key,
                    value=key,
                    variable=self.selected_keyname,
                    command=self.trigger_event("on_click_keybutton"),
                )
                for key in keys
            ]
            for keygroup, keys in zip(self._keygroups, KEY_DEFAULTS, strict=False)
        ]

        for keygroup in self._keygroups:
            keygroup.pack(side=tk.LEFT, anchor=tk.NW)

        for keybuttons in self._keybuttons:
            for btn in keybuttons:
                btn.pack(side=tk.TOP, anchor=tk.NW)

    def default(self) -> None:
        self.selected_keyname.set("C")

    def set_callback_on_click_keybutton(self, callback: t.Callable[[], t.Any]) -> None:
        self.bind_callback("on_click_keybutton", callback)

    @property
    def keyname(self) -> str:
        return self.selected_keyname.get()
