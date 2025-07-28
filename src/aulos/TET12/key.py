from aulos._core import BaseKey

from .pitchclass import PitchClass


class Key(
    BaseKey[PitchClass],
    accidental=1,
    pitchclass=PitchClass,
):
    """
    Represents a musical key in a theoretical context.

    This class extends the BaseKey and is associated with a specific PitchClass.
    It provides functionality to define and manipulate musical keys, including handling accidentals.
    """
