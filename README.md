# aulos

Python library for speech processing and analysis from a music theory perspective.

| | |
| --- | --- |
| CI/CD | [![Test](https://github.com/Oujox/aulos/actions/workflows/ci.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/ci.yml) [![Build & Publish](https://github.com/Oujox/aulos/actions/workflows/cd.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/cd.yml) |
| Package | [![pypi - version](https://img.shields.io/pypi/v/aulos.svg?&label=PyPI)](https://pypi.org/project/aulos/) [![pypi - python versions](https://img.shields.io/pypi/pyversions/aulos.svg?&label=Python)](https://pypi.org/project/aulos/) |
| Meta | [![codecov](https://codecov.io/gh/Oujox/aulos/graph/badge.svg?token=UP6ZQP7HMK)](https://codecov.io/gh/Oujox/aulos) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/aulos/blob/main/LICENSE)  |

## Features ✨

- Comprehensive tools for audio processing and analysis based on music theory principles.
- A structured framework for organizing and working with music theory objects.
- Flexible and extensible design, allowing seamless customization and expansion.

## Installation 🛠️

Install the package using pip:
```
pip install aulos
```

## Usage 📖

```python
from aulos.TET12 import Note, PitchClass

print(Note("C#4"))
# stdout:
# <Note: C#4, scale: None>

print(PitchClass("C#"))
# stdout:
# <PitchClass: C#, scale: None>
```

```python
from aulos.TET12 import Key
from aulos.TET12 import Major, Dorian, Pentatonic

print(Major(Key("C")))
# stdout:
# <Major: <Key: C>>

print(Dorian(Key("C")).components)
# stdout:
# (<PitchClass: C, scale: <Dorian: <Key: C>>>,
#  <PitchClass: D, scale: <Dorian: <Key: C>>>,
#  <PitchClass: Eb, scale: <Dorian: <Key: C>>>,
#  <PitchClass: F, scale: <Dorian: <Key: C>>>,
#  <PitchClass: G, scale: <Dorian: <Key: C>>>,
#  <PitchClass: A, scale: <Dorian: <Key: C>>>,
#  <PitchClass: Bb, scale: <Dorian: <Key: C>>>)

print(Pentatonic(Key("C")).components)
# stdout:
# (<PitchClass: C, scale: <Pentatonic: <Key: C>>>,
#  <PitchClass: D, scale: <Pentatonic: <Key: C>>>,
#  <PitchClass: E, scale: <Pentatonic: <Key: C>>>,
#  <PitchClass: G, scale: <Pentatonic: <Key: C>>>,
#  <PitchClass: A, scale: <Pentatonic: <Key: C>>>)
```

```python
from aulos.TET12 import Chord
from aulos.TET12 import Major

print(Chord("C").components)
# stdout:
# (<Note: ['Dbb4', 'C4', 'B#3', 'A###3'], scale: None>,
#  <Note: ['Gbbb4', 'Fb4', 'E4', 'D##4'], scale: None>,
#  <Note: ['Abb4', 'G4', 'F##4', 'E###4'], scale: None>)

print(Chord("CM7", scale=Major("C")).components)
# stdout:
# (<Note: C4, scale: <Major: <Key: C>>>,
#  <Note: E4, scale: <Major: <Key: C>>>,
#  <Note: G4, scale: <Major: <Key: C>>>,
#  <Note: B4, scale: <Major: <Key: C>>>)
```

```python
from aulos.TET12 import Note
from aulos.TET12 import JustIntonationTuner, Equal12Tuner

print(Note("C4", tuner=Equal12Tuner(440)).hz)
# stdout:
# 440.0

print(Note("A4", tuner=JustIntonationTuner(440)).hz)
# stdout:
# 733.3333333333333
```

## Dependencies 🧩

This project uses the following libraries and tools for development and testing.

### Runtime Dependencies 📂
This project's final product depends only on Python's **standard library**. No third-party libraries are required at runtime.


### Development Libraries 🛠️

The following libraries are used during development and testing **but are not included in the final product**

- [**pytest**](https://docs.pytest.org/en/latest/)
- [**pytest-cov**](https://github.com/pytest-dev/pytest-cov)
- [**ruff**](https://docs.astral.sh/ruff)
- [**mypy**](https://www.mypy-lang.org/)

### GitHub Actions ⚙️

- [**robvanderleek/create-issue-branch**](https://github.com/robvanderleek/create-issue-branch)
- [**release-drafter/release-drafter**](https://github.com/release-drafter/release-drafter)
- [**pypa/gh-action-pypi-publish**](https://github.com/pypa/gh-action-pypi-publish)
- [**codecov/codecov-action**](https://github.com/codecov/codecov-action)

## License 📜

This project is distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/Oujox/aulos/blob/main/LICENSE) file.

## Contact 📬

- Email: oujoxyz365@gmail.com
