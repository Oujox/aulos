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
    _selected_keyname: tk.StringVar

    _keyselecter_wrap: ttk.Frame
    _keyselecter_title: ttk.Label
    _keygroups: list[ttk.Frame]
    _keybuttons: list[list[ttk.Radiobutton]]

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master
        self.create_widget()

    def create_widget(self) -> None:
        self._selected_keyname = tk.StringVar()
        self._keyselecter_wrap = ttk.Frame(
            self,
            padding=(24, 8),
            borderwidth=2,
            relief=tk.SOLID,
        )
        self._keyselecter_title = ttk.Label(self, text="Key")
        self._keyselecter_wrap.pack()
        self._keyselecter_title.place(relx=0.05, rely=0, anchor=tk.W)

        self._keygroups = [ttk.Frame(self._keyselecter_wrap, padding=(6, 0)) for _ in range(len(KEY_DEFAULTS))]
        self._keybuttons = [
            [
                ttk.Radiobutton(
                    keygroup,
                    text=key,
                    value=key,
                    variable=self._selected_keyname,
                    command=self._on_click_keybutton,
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
        self._selected_keyname.set("C")
        self._on_click_keybutton()

    def _on_click_keybutton(self) -> None:
        for callback in self.callbacks_on_click_keybutton:
            callback()

    @property
    def keyname(self) -> str:
        return self._selected_keyname.get()

    callbacks_on_click_keybutton: list[t.Callable[[], t.Any]]

    def set_callback_on_click_keybutton(self, callback: t.Callable[[], t.Any]) -> None:
        if not hasattr(self, "callbacks_onClickKeyButton"):
            self.callbacks_on_click_keybutton = []
        self.callbacks_on_click_keybutton.append(callback)
