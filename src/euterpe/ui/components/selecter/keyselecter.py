import tkinter as tk
import tkinter.ttk as ttk
import typing as t

from ...const import KEY_DEFAULTS
from ..base import BaseComponent


class KeySelecter(BaseComponent):

    _selected_keyname: tk.StringVar

    _keyselecter_wrap: ttk.Frame
    _keyselecter_title: ttk.Label
    _keygroups: list[ttk.Frame]
    _keybuttons: list[list[ttk.Radiobutton]]

    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.master = master
        self.create_widget()

    def create_widget(self):
        self._selected_keyname = tk.StringVar()
        self._keyselecter_wrap = ttk.Frame(
            self, padding=(24, 8), borderwidth=2, relief=tk.SOLID
        )
        self._keyselecter_title = ttk.Label(self, text="Key")
        self._keyselecter_wrap.pack()
        self._keyselecter_title.place(relx=0.05, rely=0, anchor=tk.W)

        self._keygroups = [
            ttk.Frame(self._keyselecter_wrap, padding=(6, 0))
            for _ in range(len(KEY_DEFAULTS))
        ]
        self._keybuttons = [
            [
                ttk.Radiobutton(
                    keygroup,
                    text=key,
                    value=key,
                    variable=self._selected_keyname,
                    command=self._onClickKeyButton,
                )
                for key in keys
            ]
            for keygroup, keys in zip(self._keygroups, KEY_DEFAULTS)
        ]

        for keygroup in self._keygroups:
            keygroup.pack(side=tk.LEFT, anchor=tk.NW)

        for keybuttons in self._keybuttons:
            for btn in keybuttons:
                btn.pack(side=tk.TOP, anchor=tk.NW)

    def default(self):
        self._selected_keyname.set("C")
        self._onClickKeyButton()

    def _onClickKeyButton(self):
        for callback in self.callbacks_onClickKeyButton:
            callback()

    @property
    def keyname(self):
        return self._selected_keyname.get()

    callbacks_onClickKeyButton: list[t.Callable[[], t.Any]]

    def set_callback_onClickKeyButton(self, callback: t.Callable[[], t.Any]):
        if not hasattr(self, "callbacks_onClickKeyButton"):
            self.callbacks_onClickKeyButton = []
        self.callbacks_onClickKeyButton.append(callback)
