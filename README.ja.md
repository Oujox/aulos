# aulos

[English](https://github.com/Oujox/aulos/blob/main/README.md) | 日本語

> [!WARNING]
>
> Aulos は現在開発中です。API は変更される可能性があります。

音高・和音・音階、調律、リズムを扱う Python ライブラリ。
記譜・調律・表示を分離し、音程比と時間を有理数で表します。

Aulos は作者と AI による共作です。

Python 3.13+ · 必須依存なし · [MIT License](https://github.com/Oujox/aulos/blob/main/LICENCE)

```sh
pip install aulos
```

| | |
| --- | --- |
| CI/CD | [![CI](https://github.com/Oujox/aulos/actions/workflows/ci.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/ci.yml) [![CD](https://github.com/Oujox/aulos/actions/workflows/cd.yml/badge.svg)](https://github.com/Oujox/aulos/actions/workflows/cd.yml) |
| Package | [![pypi - version](https://img.shields.io/pypi/v/aulos.svg?&label=PyPI)](https://pypi.org/project/aulos/) [![pypi - python versions](https://img.shields.io/pypi/pyversions/aulos.svg?&label=Python)](https://pypi.org/project/aulos/) |
| Meta | [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat)](https://github.com/Oujox/aulos/blob/main/LICENCE)  |

## 公開 API

| モジュール | 内容 |
| --- | --- |
| `aulos.western.equal` | 西洋式七文字記譜・12平均律 |
| `aulos.western.just` | 西洋式七文字記譜・5リミット純正律 |
| `aulos.pentatonic` | 独立した五文字連鎖記譜。周波数の評価時に調律を指定 |
| `aulos.rhythm` | 音価・時刻・拍子・周期・時間構造 |
| `aulos.base` | 独自の記譜体系・調律・表示規約を定義する部品 |

各モジュールの `__all__` と、公開クラスの `_` で始まらない属性が公開対象です。
`aulos.core` は非公開の実装です。

## 音高・和音・音階

三つの記譜体系は、共通の `PitchClass`・`Pitch`・`Voicing`・`Chord`・`Scale` を公開します。

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
Voicing("m7").at(Pitch("D4"))       # D4・F4・A4・C5 の Pitch

scale = Scale("C major")
scale.chord(1, count=4).names        # ('D4', 'F4', 'A4', 'C5')
str(scale.mode(1))                  # 'D dorian'
```

| API | 主な操作・属性 |
| --- | --- |
| `PitchClass` | `from_spelling()`、音程の加減算 |
| `Pitch` | `from_class()`、`pitch_class`、`register`、`frequency()`、`enharmonics()` |
| `Chord` / `Scale` | `members`、`names`、`intervals`、`transpose()`、`frequencies()`、`from_members()`、`from_intervals()` |
| `Chord` | `root`、`bass`、`voicing`、`inversion()`、`over()` |
| `Scale` | `tonic`、`degrees`、`degree()`、`degree_of()`、`mode()`、`chord()` |
| `Voicing` | `intervals`、`at()`、`from_intervals()` |

`Chord.templates.names` / `Scale.templates.names` で利用できる名前を確認できます。
`template_name` は音程比まで、`structure_name` は綴りで照合した名前です。

## 音程比と調律

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

`ratio()` は記譜上の比、`cents()` / `frequency()` / `frequencies()` は調律後の値を返します。

## リズムと時間構造

```python
from fractions import Fraction

from aulos.rhythm import Cycle, Duration, Event, Meter, NoteValue, Tempo
from aulos.western.equal import Chord, Pitch

quarter = Duration(Fraction(1, 4))
eighth = Duration(Fraction(1, 8))

NoteValue.of(quarter + eighth)       # 付点四分音符
Meter((2, 3), eighth).weights        # (2, 0, 0, 1, 0, 0): 6/8
Cycle.euclidean(8, 3).steps          # (2, 3, 3)

melody = Event(quarter, Pitch("E4")) + Event(eighth) + Event(eighth, Pitch("G4"))
phrase = melody | Event(quarter * 2, Chord("C/E"))
phrase.events()                    # 開始時刻・音価・値の列
Tempo(quarter, 120.0).seconds(phrase.duration)  # 1.0
```

| API | 用途 |
| --- | --- |
| `Duration` / `Position` | 音価と時刻、有理数での演算 |
| `NoteValue` / `Meter` | 音符・付点・連符、拍子と拍の強弱 |
| `Cycle` | 周期パターン、`rotate()`、`mode()`、`repeat()`、和集合 `\|`・積集合 `&` |
| `Part` / `Event` / `Serial` / `Parallel` / `Placed` | 任意の値を置く時間構造。直列 `+`・並列 `\|`、`events()`、`stretch()`、`map()` |
| `Tempo` / `TempoMap` | 一定・可変テンポでの秒への変換 |
| `RhythmError` | 拍子・周期の不整合を表す例外 |

## 独自の体系

`aulos.base` の公開 API:

| 用途 | 名前 |
| --- | --- |
| 体系と基底クラス | `Tag`、`NotationTag`、`Definition`、`PitchClass`、`Pitch`、`Voicing`、`Chord`、`Scale` |
| 記譜と音程 | `ChainNotation`、`ChainInterval`、`Notation`、`Interval`、`Quality`、`Comma` |
| 表示 | `Symbols`、`CommaSymbols` |
| 調律 | `Temperament`、`Tuning` |
| 名前と音程列 | `Template`、`Templates`、`Realization` |
| 例外 | `NotationError`、`TemperamentError`、`RepresentationError` |

サンプル: [表示規約](https://github.com/Oujox/aulos/blob/main/examples/custom_symbols.py) · [調律](https://github.com/Oujox/aulos/blob/main/examples/custom_tuning.py) · [五文字記譜](https://github.com/Oujox/aulos/blob/main/examples/five_letters.py) · [リズム](https://github.com/Oujox/aulos/blob/main/examples/rhythm.py)
