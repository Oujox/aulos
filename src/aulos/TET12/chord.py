from aulos._core import BaseChord

from .note import Note


class Chord(
    BaseChord[Note],
    qualities=(
        # Triads
        {"name": "", "positions": (0, 4, 7), "areas": ("maj",)},
        {"name": "m", "positions": (0, 3, 7)},
        {"name": "sus2", "positions": (0, 2, 7)},
        {"name": "sus4", "positions": (0, 5, 7)},
        {"name": "dim", "positions": (0, 3, 6)},
        {"name": "aug", "positions": (0, 4, 8)},
        # Seventh Chords
        {"name": "6", "positions": (0, 4, 7, 9)},
        {"name": "7", "positions": (0, 4, 7, 10)},
        {"name": "M7", "positions": (0, 4, 7, 11)},
        {"name": "m6", "positions": (0, 3, 7, 9)},
        {"name": "m7", "positions": (0, 3, 7, 10)},
        {"name": "mM7", "positions": (0, 3, 7, 11)},
        {"name": "dim7", "positions": (0, 3, 6, 9)},
        {"name": "m7b5", "positions": (0, 3, 6, 10)},
        # Altered Chords
    ),
    note=Note,
):
    """
    Represents a musical chord, which is a combination of notes played simultaneously.

    This class extends the BaseChord and provides specific qualities and positions for various chord types,
    including triads, seventh chords, and altered chords. It allows for the representation and manipulation
    of chords in a musical context, using the Note class for individual notes.
    """
