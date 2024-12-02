# aulos

A Python library for exploring and utilizing music theory concepts in an intuitive and programmatic way.

[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/aulos/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Oujox/aulos/graph/badge.svg?token=UP6ZQP7HMK)](https://codecov.io/gh/Oujox/aulos)

> **workflows**
>
> [![🐍 Python Tests Workflow](https://github.com/Oujox/aulos/actions/workflows/test-python.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/test-python.yml)

## overview

## install

## usage

```python
from aulos import Note

a1 = Note("A4")

print(a1)
>> <Note: 'A4'>
```

```python
from aulos import scale, Key

c = Key("C")

major = scale.Major(c)
locrian = scale.Locrian(c)

print(major)
>> <Scale: 'Major'>

print(locrian.diatonics)
>> ['C','D','E','F','G','A','B']
```

```python
from aulos import Chord

cm7b5 = Chord("Cm7b5")

print(cm7b5)
```

```python
from aulos import Progress

cm7b5 = Progress(["F", "E7", "Am", "G"])
```

## Lisence

This project is distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/Oujox/aulos/blob/main/LICENSE) file.
