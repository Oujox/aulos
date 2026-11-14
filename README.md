# aulos

English | [日本語](https://github.com/Oujox/aulos/blob/main/README.ja.md)

A Python library for pitches, chords, scales, tuning, and rhythm.
Notation, tuning, and display are defined separately, with exact rational values for interval ratios and time.

Python 3.13+ · No runtime dependencies · [MIT License](https://github.com/Oujox/aulos/blob/main/LICENCE)

```sh
pip install aulos
```

| | |
| --- | --- |
| CI/CD | [![CI](https://github.com/Oujox/aulos/actions/workflows/ci.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/ci.yml) [![CD](https://github.com/Oujox/aulos/actions/workflows/cd.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/cd.yml) |
| Package | [![pypi - version](https://img.shields.io/pypi/v/aulos.svg?&label=PyPI)](https://pypi.org/project/aulos/) [![pypi - python versions](https://img.shields.io/pypi/pyversions/aulos.svg?&label=Python)](https://pypi.org/project/aulos/) |
| Meta | [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/aulos/blob/main/LICENCE)  |

## Public API

| Module | Purpose |
| --- | --- |
| `aulos.western.equal` | Western seven-letter notation with 12-tone equal temperament |
| `aulos.western.just` | Western seven-letter notation with 5-limit just intonation |
| `aulos.pentatonic` | An independent five-letter chain notation; supply a tuning to evaluate frequencies |
| `aulos.rhythm` | Durations, positions, meter, cycles, and temporal structure |
| `aulos.base` | Building blocks for custom notation, tuning, and display conventions |

The public API consists of the names in each module's `__all__` and attributes of public classes that do not start with `_`.
`aulos.core` is internal.

## Pitches, chords, and scales

All three notation systems expose `PitchClass`, `Pitch`, `Voicing`, `Chord`, and `Scale` with a shared interface.

```python
from aulos.western.equal import Chord, Pitch, PitchClass, Scale, Voicing

pitch = Pitch("C#4")
pitch.pitch_class == PitchClass("C#")  # True
pitch.frequency(Pitch("A4"), 440.0)

fifth = Pitch("G4") - Pitch("C4")
str(Pitch("C4") + fifth)  # 'G4'

chord = Chord("Cm7")
chord.names                         # ('C4', 'Eb4', 'G4', 'Bb4')
chord.inversion(1).names            # ('Eb4', 'G4', 'Bb4', 'C5')
chord.transpose(fifth)
Voicing("m7").at(Pitch("D4"))       # Pitch objects for D4, F4, A4, C5

scale = Scale("C major")
scale.chord(1, count=4).names        # ('D4', 'F4', 'A4', 'C5')
str(scale.mode(1))                  # 'D dorian'
```

| API | Key operations and attributes |
| --- | --- |
| `PitchClass` | `from_spelling()`, interval addition and subtraction |
| `Pitch` | `from_class()`, `pitch_class`, `register`, `frequency()`, `enharmonics()` |
| `Chord` / `Scale` | `members`, `names`, `intervals`, `transpose()`, `frequencies()`, `from_members()`, `from_intervals()` |
| `Chord` | `root`, `bass`, `voicing`, `inversion()`, `over()` |
| `Scale` | `tonic`, `degrees`, `degree()`, `degree_of()`, `mode()`, `chord()` |
| `Voicing` | `intervals`, `at()`, `from_intervals()` |

Use `Chord.templates.names` / `Scale.templates.names` to list available names.
`template_name` matches exact interval ratios; `structure_name` matches interval spellings.

## Interval ratios and tuning

```python
from fractions import Fraction

from aulos.base import Temperament, Tuning
from aulos.western.just import Chord

chord = Chord("Cm7")
chord.names  # ('C4', 'Eb4↑', 'G4', 'Bb4↑')
tuple(interval.ratio() for interval in chord.intervals)  # (1, 6/5, 3/2, 9/5)

fifth = chord.notation.interval(Fraction(3, 2))
fifth.cents(chord.tuning)
chord.frequencies(chord.root, 261.626)

edo19 = Tuning(Temperament.equal_division((2, 3, 5), 19, Fraction(2)), (1200 / 19,))
chord.frequencies(chord.root, 261.626, edo19)
```

`ratio()` returns the notated ratio; `cents()` / `frequency()` / `frequencies()` evaluate it under a tuning.

## Rhythm and time

```python
from fractions import Fraction

from aulos.rhythm import Cycle, Duration, Event, Meter, NoteValue, Tempo
from aulos.western.equal import Chord, Pitch

quarter = Duration(Fraction(1, 4))
eighth = Duration(Fraction(1, 8))

NoteValue.of(quarter + eighth)       # Dotted quarter note
Meter((2, 3), eighth).weights        # (2, 0, 0, 1, 0, 0): 6/8
Cycle.euclidean(8, 3).steps          # (2, 3, 3)

melody = Event(quarter, Pitch("E4")) + Event(eighth) + Event(eighth, Pitch("G4"))
phrase = melody | Event(quarter * 2, Chord("C/E"))
phrase.events()                    # Events with start positions, durations, and values
Tempo(quarter, 120.0).seconds(phrase.duration)  # 1.0
```

| API | Purpose |
| --- | --- |
| `Duration` / `Position` | Durations and positions with rational arithmetic |
| `NoteValue` / `Meter` | Note values, dots, tuplets, meter, and metric weights |
| `Cycle` | Periodic patterns, `rotate()`, `mode()`, `repeat()`, union `\|`, and intersection `&` |
| `Part` / `Event` / `Serial` / `Parallel` / `Placed` | Temporal structures holding arbitrary values: sequence `+`, parallel composition `\|`, `events()`, `stretch()`, `map()` |
| `Tempo` / `TempoMap` | Conversion to seconds at constant or changing tempos |
| `RhythmError` | Errors in meter or cycle operations |

## Custom systems

Public API in `aulos.base`:

| Purpose | Names |
| --- | --- |
| System definitions and base classes | `Tag`, `NotationTag`, `Definition`, `PitchClass`, `Pitch`, `Voicing`, `Chord`, `Scale` |
| Notation and intervals | `ChainNotation`, `ChainInterval`, `Notation`, `Interval`, `Quality`, `Comma` |
| Display | `Symbols`, `CommaSymbols` |
| Tuning | `Temperament`, `Tuning` |
| Named interval structures | `Template`, `Templates`, `Realization` |
| Exceptions | `NotationError`, `TemperamentError`, `RepresentationError` |

Examples: [Display conventions](https://github.com/Oujox/aulos/blob/main/examples/custom_symbols.py) · [Tuning](https://github.com/Oujox/aulos/blob/main/examples/custom_tuning.py) · [Five-letter notation](https://github.com/Oujox/aulos/blob/main/examples/five_letters.py) · [Rhythm](https://github.com/Oujox/aulos/blob/main/examples/rhythm.py)
