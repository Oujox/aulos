# aulos

Python library for speech processing and analysis from a music theory perspective.

| | |
| --- | --- |
| CI/CD | [![Test](https://github.com/Oujox/aulos/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Oujox/aulos/actions/workflows/ci.yml) [![Build & Publish](https://github.com/Oujox/aulos/actions/workflows/cd.yml/badge.svg?branch=main)](https://github.com/Oujox/aulos/actions/workflows/cd.yml) |
| Package |  |
| Meta | [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy) [![codecov](https://codecov.io/gh/Oujox/aulos/graph/badge.svg?token=UP6ZQP7HMK)](https://codecov.io/gh/Oujox/aulos) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/aulos/blob/main/LICENSE) |

## Features ✨

- Comprehensive tools for audio processing and analysis based on music theory principles.
- A structured framework for organizing and working with music theory objects.
- Flexible and extensible design, allowing seamless customization and expansion.

## Installation 🛠️

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
- [**actions/checkout**](https://github.com/actions/checkout)
- [**actions/setup-python**](https://github.com/actions/setup-python)
- [**actions/upload-artifact**](https://github.com/actions/upload-artifact)
- [**actions/download-artifact**](https://github.com/actions/download-artifact)

## License 📜

This project is distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/Oujox/aulos/blob/main/LICENSE) file.

## Contact 📬

- Email: oujoxyz365@gmail.com
