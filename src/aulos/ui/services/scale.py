import typing as t

from aulos import Scale
from aulos.TET12 import Key, scale


class ScaleService:
    SCALES_BY_TET12: t.ClassVar[tuple[dict[str, type[Scale]], dict[str, type[Scale]]]] = (
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

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)

    def get_key_names(self) -> tuple[str, ...]:
        return Key.schema.keynames

    def get_scale_names(self) -> tuple[str, ...]:
        return self.get_tonalscalenames() + self.get_modalscalenames()

    def get_tonalscalenames(self) -> tuple[str, ...]:
        return tuple(self.SCALES_BY_TET12[0].keys())

    def get_modalscalenames(self) -> tuple[str, ...]:
        return tuple(self.SCALES_BY_TET12[1].keys())

    def get_scale(self, scalename: str) -> type[Scale]:
        if scalename in self.SCALES_BY_TET12[0]:
            return self.SCALES_BY_TET12[0][scalename]
        return self.SCALES_BY_TET12[1][scalename]
