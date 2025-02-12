import argparse as ap
import tkinter as tk
import typing as t
from pprint import pprint

from aulos.ui.components import KeySelecter, ScaleDisplay, ScaleSelecter
from aulos.ui.services import ScaleService

from .base import BaseCLI


def build_scaleviewer_gui() -> None:
    root = tk.Tk()
    root.title("ScaleViewer GUI")
    root.geometry("700x700")
    root.resizable(width=False, height=False)

    scaledisplay = ScaleDisplay(root)
    keyselecter = KeySelecter(root)
    scaleselecter = ScaleSelecter(root)

    def display_scaledisplay() -> None:
        scaledisplay.keyname = keyselecter.keyname
        scaledisplay.scalename = scaleselecter.scalename
        scaledisplay.scaleinfo = scaleselecter.scaleinfo

    keyselecter.set_callback_on_click_keybutton(display_scaledisplay)
    scaleselecter.set_callback_on_click_scalebutton(display_scaledisplay)

    scaledisplay.create_widget()
    keyselecter.create_widget()
    scaleselecter.create_widget()
    keyselecter.default()
    scaleselecter.default()
    display_scaledisplay()
    scaledisplay.pack(side=tk.TOP, anchor=tk.W, expand=True)
    keyselecter.pack(side=tk.LEFT, anchor=tk.N)
    scaleselecter.pack(side=tk.LEFT, anchor=tk.N)

    root.mainloop()


class ScaleViewer(BaseCLI):
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
        parser.add_argument(
            "--gui",
            action="store_true",
            help="display the scale viewer in a GUI",
        )

    def execute(self, args: ap.Namespace) -> None:
        key = args.key
        scale = args.scale

        if args.gui:
            build_scaleviewer_gui()
            return

        components = self.service.get_scale(scale)(key).components
        print("key:", key)  # noqa: T201
        print("scale:", scale)  # noqa: T201
        pprint(components)  # noqa: T203
