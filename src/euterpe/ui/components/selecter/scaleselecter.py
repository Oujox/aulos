import tkinter as tk
import tkinter.ttk as ttk
import typing as t

from euterpe import _Scale
from euterpe.TET12 import scale

from ..base import BaseComponent

SCALE_DEFAULTS: tuple[dict[str, type[_Scale]], dict[str, type[_Scale]]] = (
    {
        scale.Major.__name__: scale.Major,
        scale.Minor.__name__: scale.Minor,
        scale.MelodicMinor.__name__: scale.MelodicMinor,
        scale.HarmonicMinor.__name__: scale.HarmonicMinor,
        scale.Pentatonic.__name__: scale.Pentatonic,
        scale.MinorPentatonic.__name__: scale.MinorPentatonic,
        scale.Diminish.__name__: scale.Diminish,
        scale.CombDiminish.__name__: scale.CombDiminish,
        scale.Wholetone.__name__: scale.Wholetone,
        scale.Bluenote.__name__: scale.Bluenote,
    },
    {
        scale.Aeorian.__name__: scale.Aeorian,
        scale.Aeorian_f5.__name__: scale.Aeorian_f5,
        scale.AlteredSuperLocrian.__name__: scale.AlteredSuperLocrian,
        scale.Dorian.__name__: scale.Dorian,
        scale.Dorian_f2.__name__: scale.Dorian_f2,
        scale.Dorian_s4.__name__: scale.Dorian_s4,
        scale.Ionian.__name__: scale.Ionian,
        scale.Ionian_s5.__name__: scale.Ionian_s5,
        scale.Locrian.__name__: scale.Locrian,
        scale.Locrian_n6.__name__: scale.Locrian_n6,
        scale.Lydian.__name__: scale.Lydian,
        scale.Lydian_f7.__name__: scale.Lydian_f7,
        scale.Lydian_s2.__name__: scale.Lydian_s2,
        scale.Lydian_s5.__name__: scale.Lydian_s5,
        scale.Mixolydian.__name__: scale.Mixolydian,
        scale.Mixolydian_f6.__name__: scale.Mixolydian_f6,
        scale.Mixolydian_f9.__name__: scale.Mixolydian_f9,
        scale.Phrygian.__name__: scale.Phrygian,
        scale.SuperLocrian.__name__: scale.SuperLocrian,
    },
)


class ScaleSelecter(BaseComponent):

    _selected_scalename: tk.StringVar
    _selected_scaleinfo: tk.StringVar

    _scaleselecter_wrap: ttk.Frame
    _scalesetecter_title: ttk.Label
    _scalegroups: list[ttk.Frame]
    _scalebuttons: list[list[ttk.Radiobutton]]

    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.master = master
        self.create_widget()

    def create_widget(self):

        self._selected_scalename = tk.StringVar()
        self._selected_scaleinfo = tk.StringVar()

        self._scaleselecter_wrap = ttk.Frame(
            self, padding=(24, 8), borderwidth=2, relief=tk.SOLID
        )
        self._scalesetecter_title = ttk.Label(self, text="Scale")
        self._scaleselecter_wrap.pack()
        self._scalesetecter_title.place(relx=0.05, rely=0, anchor=tk.W)

        self._scalegroups = [
            ttk.Frame(self._scaleselecter_wrap, padding=(6, 0))
            for _ in range(len(SCALE_DEFAULTS))
        ]
        self._scalebuttons = [
            [
                ttk.Radiobutton(
                    scalegroup,
                    text=scale,
                    value=scale,
                    variable=self._selected_scalename,
                    command=self._onClickScaleButton,
                )
                for scale in scales.keys()
            ]
            for scalegroup, scales in zip(self._scalegroups, SCALE_DEFAULTS)
        ]

        for scalegroup in self._scalegroups:
            scalegroup.pack(side=tk.LEFT, anchor=tk.NW)

        for scalebuttons in self._scalebuttons:
            for btn in scalebuttons:
                btn.pack(side=tk.TOP, anchor=tk.NW)

    def default(self):
        self._selected_scalename.set(scale.Major.__name__)
        self._onClickScaleButton()

    def _onClickScaleButton(self):
        for scales in SCALE_DEFAULTS:
            name = self._selected_scalename.get()
            if name in scales:
                self._selected_scaleinfo.set(scales[name].__doc__ or "")

        for callback in self.callbacks_onClickScaleButton:
            callback()

    @property
    def scale(self) -> type[_Scale] | None:
        for scales in SCALE_DEFAULTS:
            if self.scalename in scales:
                return scales[self.scalename]
        return None

    @property
    def scalename(self) -> str:
        return self._selected_scalename.get()

    @property
    def scaleinfo(self) -> str:
        return self._selected_scaleinfo.get()

    callbacks_onClickScaleButton: list[t.Callable[[], t.Any]]

    def set_callback_onClickScaleButton(self, callback: t.Callable[[], t.Any]):
        if not hasattr(self, "callbacks_onClickScaleButton"):
            self.callbacks_onClickScaleButton = []
        self.callbacks_onClickScaleButton.append(callback)
