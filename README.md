# euterpe

Python library for speech processing and analysis from a music theory perspective.

[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/euterpe/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Oujox/euterpe/graph/badge.svg?token=UP6ZQP7HMK)](https://codecov.io/gh/Oujox/euterpe)

[![🐍 Python Tests Workflow](https://github.com/Oujox/euterpe/actions/workflows/test-python.yml/badge.svg)](https://github.com/Oujox/euterpe/actions/workflows/test-python.yml)

## Features ✨

- Comprehensive tools for audio processing and analysis based on music theory principles.
- A structured framework for organizing and working with music theory objects.
- Flexible and extensible design, allowing seamless customization and expansion.

## Installation 🛠️

## Usage 📖

1. a
```python
import wave
from euterpe import Euterpe

euterpe = Euterpe("my")

@euterpe.Track()
def track():
    return wave.open(path, "rb")

track().play()
```

2. 
```python
from euterpe import scale, Key

c = Key("C")

major = scale.Major(c)
locrian = scale.Locrian(c)

print(major)
>> <Scale: 'Major'>

print(locrian.diatonics)
>> ['C','D','E','F','G','A','B']
```

```python
from euterpe import Chord

cm7b5 = Chord("Cm7b5")

print(cm7b5)
```

```python
from euterpe import Progress

cm7b5 = Progress(["F", "E7", "Am", "G"])
```

## Documentation 📚

## License 📜

This project is distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/Oujox/euterpe/blob/main/LICENSE) file.

## Contact 📬
