# Chordal

A Python library for exploring and utilizing music theory concepts in an intuitive and programmatic way.

[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/Chordal/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/Oujox/Chordal/graph/badge.svg?token=UP6ZQP7HMK)](https://codecov.io/gh/Oujox/Chordal)

> **workflows**
>
> [![🐍 Python Tests Workflow](https://github.com/Oujox/Chordal/actions/workflows/test-python.yml/badge.svg)](https://github.com/Oujox/Chordal/actions/workflows/test-python.yml)

## overview

## install

## usage

```python
from chordal import PitchClass

c = PitchClass("C")
```

```python
from chordal import Note

c = Note("C1")
```

```python
from chordal import Major, Locrian, Key

c = Key("C")

major = Major(c)
locrian = Locrian(c)
```

```python
from chordal import Chord

cm7b5 = Chord("Cm7b5")
```

```python
from chordal import Progress

cm7b5 = Progress(["F", "E7", "Am", "G"])
```

## Lisence

This project is distributed under the MIT License. For more information, refer to the [LICENSE](https://github.com/Oujox/Chordal/blob/main/LICENSE) file.
