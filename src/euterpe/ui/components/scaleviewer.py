import typing as t
import tkinter as tk
import tkinter.ttk as ttk

from ..const import KEY_DEFAULTS


class ScaleViewer(tk.Frame):

    selected_keyname: tk.StringVar
    selected_scalename: tk.StringVar

    keyselecter: ttk.Frame
    keyselecter_title: ttk.Label
    keygroup: list[ttk.Frame]
    keybuttons: list[list[ttk.Radiobutton]]
    
    scalesetecter: ttk.Frame
    scalesetecter_title: ttk.Label
    scale_listbox: tk.Listbox

    def __init__(self, master: tk.Misc):
        super().__init__(master, pady=6)
        self.master = master
        self.create_widget()

    def create_widget(self):
        self._create_scaledisplay()
        self._create_keyselecter()
        self._create_scaleselecter()

    def _create_scaledisplay(self):
        ...
    
    def _create_keyselecter(self):
        self.selected_keyname = tk.StringVar()

        self.keyselecter = ttk.Frame(self, padding=(24, 8), borderwidth=2, relief=tk.SOLID)
        self.keyselecter_title = ttk.Label(self, text="Key")
        self.keyselecter_title.place(relx=0.05, rely=0, anchor=tk.W)

        self.keygroup = [
            ttk.Frame(self.keyselecter, padding=(6, 0)) for _ in range(3)
        ]
        self.keybuttons = [
            [ttk.Radiobutton(
                keygroup,
                text=key,
                value=key,
                variable=self.selected_keyname
            )
            for key in keys]
            for keygroup, keys in zip(self.keygroup, KEY_DEFAULTS)
        ]

        for keygroup in self.keygroup:
            keygroup.pack(side=tk.LEFT)

        for keybuttons in self.keybuttons:
            for btn in keybuttons:
                btn.pack(side=tk.TOP)

        self.keyselecter.pack()
    
    def _create_scaleselecter(self):
        ...
