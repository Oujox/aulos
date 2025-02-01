import tkinter as tk
import typing as t
from tkinter import ttk

from aulos.ui.const import KEYBOARD_BLACK_CLASSES, KEYBOARD_WHITE_CLASSES


class KeyElement(tk.Frame):
    key: tk.Button
    is_active: tk.BooleanVar

    notenumber: int

    def __init__(self, master: tk.Misc, notenumber: int, *, width: int, height: int) -> None:
        super().__init__(master)
        self.master = master
        self.notenumber = notenumber
        self.create_widget(width, height)

    def create_widget(self, width: int, height: int) -> None:
        if self.is_white():
            self.key = tk.Button(self)
            self.key.config(bg="#FFFFFF")
            self.config(width=width, height=height)
            self.key.place(x=0, y=0, anchor=tk.NW, width=width, height=height)

        elif self.is_black():
            self.key = tk.Button(self)
            self.key.config(bg="#000000")
            self.config(width=width * (2 / 3), height=height * (2 / 3))
            self.key.place(
                x=0,
                y=0,
                anchor=tk.NW,
                width=width * (2 / 3),
                height=height * (2 / 3),
            )

        def callback_btn_bgcolor(*_args: t.Any) -> None:
            if self.is_active.get():
                self.key.config(bg="#FF6347")
            elif self.is_white():
                self.key.config(bg="#FFFFFF")
            elif self.is_black():
                self.key.config(bg="#000000")

        self.is_active = tk.BooleanVar(value=True)
        self.is_active.trace_add("write", callback_btn_bgcolor)

    def default(self) -> None:
        return

    def is_white(self) -> bool:
        return (self.notenumber % 12) in KEYBOARD_WHITE_CLASSES

    def is_black(self) -> bool:
        return (self.notenumber % 12) in KEYBOARD_BLACK_CLASSES


class KeyBoard(tk.Frame):
    notebook: ttk.Notebook
    tab1: tk.Frame
    tab2: tk.Frame

    canvas: tk.Canvas
    scrollbar: tk.Scrollbar

    keyboard: tk.Frame
    keylist: list[KeyElement]

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master
        self.create_widget()

    def create_widget(self) -> None:
        self.notebook = ttk.Notebook(self)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        # --- tab1 ---
        self.canvas = tk.Canvas(self.tab1, width=1000, height=72)
        self.keyboard = tk.Frame(self.canvas, width=1750, height=72, bg="#F0F0F0")
        self.scrollbar = tk.Scrollbar(
            self.tab1,
            orient=tk.HORIZONTAL,
            command=self.canvas.xview,
        )

        self.canvas.create_window((0, 0), window=self.keyboard, anchor=tk.NW)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.keyboard.bind(
            "<Configure>",
            lambda _: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.keyboard.update_idletasks()

        self.keylist = self._create_keylist()

        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # --- tab2 ---

        # ------------
        self.notebook.add(self.tab1, text="keyboard")
        self.notebook.add(self.tab2, text="⚙")
        self.notebook.pack(fill=tk.BOTH, expand=True)

    def _create_keylist(self) -> list[KeyElement]:
        x = 0
        keylist: list[KeyElement] = []

        for notenumber in range(128):
            key = KeyElement(self.keyboard, notenumber, width=24, height=72)

            if key.is_white():
                key.place(x=x, y=0, anchor=tk.NW)
                x += 24

            elif key.is_black():
                key.place(x=x, y=0, anchor=tk.N)

            keylist.append(key)

        for key in keylist[:-1]:
            if key.is_black():
                key.lift(aboveThis=keylist[-1])

        return keylist

    def default(self) -> None:
        return
