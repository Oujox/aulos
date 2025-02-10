import argparse as ap
import tkinter as tk
import typing as t
from pprint import pprint

from aulos.ui.components import KeySelecter, ScaleDisplay, ScaleSelecter
from aulos.ui.services import ScaleService

from .base import BaseCLI


class ScaleViewerGUI(tk.Frame):
    scaledisplay: ScaleDisplay
    keyselecter: KeySelecter
    scaleselecter: ScaleSelecter

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master)
        self.master = master
        self.service = ScaleService()
        self.create_widget()
        self.default()

    def create_widget(self) -> None:
        self.scaledisplay = ScaleDisplay(self)
        self.keyselecter = KeySelecter(self)
        self.scaleselecter = ScaleSelecter(self)

        self.keyselecter.set_callback_on_click_keybutton(self.display_scaledisplay)
        self.scaleselecter.set_callback_on_click_scalebutton(self.display_scaledisplay)

        self.scaledisplay.pack(side=tk.TOP, anchor=tk.W, expand=True)
        self.keyselecter.pack(side=tk.LEFT, anchor=tk.N)
        self.scaleselecter.pack(side=tk.LEFT, anchor=tk.N)

    def default(self) -> None:
        self.keyselecter.default()
        self.scaleselecter.default()

    def display_scaledisplay(self) -> None:
        self.scaledisplay.keyname = self.keyselecter.keyname
        self.scaledisplay.scalename = self.scaleselecter.scalename
        self.scaledisplay.scaleinfo = self.scaleselecter.scaleinfo


class ScaleViewerCLI(BaseCLI):
    def __init__(self, parser: ap.ArgumentParser, **kwargs: t.Any) -> None:
        super().__init__(parser, **kwargs)
        self.service = ScaleService()
        parser.add_argument(
            "key",
            nargs="?",
            default="C",
            choices=self.service.get_key_names(),
            help="the key of the scale",
        )
        parser.add_argument(
            "scale",
            nargs="?",
            default="Major",
            choices=self.service.get_scale_names(),
            help="the scale to display",
        )

    def execute(self, args: ap.Namespace) -> None:
        key = args.key
        scale = args.scale

        # print the components
        components = self.service.get_scale_components(scale, key)
        print("key:", key)  # noqa: T201
        print("scale:", scale)  # noqa: T201
        pprint(components)  # noqa: T203
