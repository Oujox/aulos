import typing as t
from functools import wraps

from .track import Track
from .._core.framework import Context
from .._core import Setting


class EuterpeTrackReturn(t.TypedDict, total=False):
    track: list[int]


class Euterpe:

    def __init__(self, name: str, *, setting: Setting | None = None):
        self.name = name
        self.setting = setting or Setting.default()

    def WorkSpace(self):
        def inner[**P](func: t.Callable[P, None]) -> t.Callable[P, None]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
                return func(*args, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner

    def Track(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Reverb(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner

    def Distortion(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Deray(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Chorus(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Flanger(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Equalizer(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Compressor(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Tremolo(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def PitchShift(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
    
    def Looper(self):
        def inner(func: t.Callable[t.Concatenate[Track, ...], Track]) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)
            return Context(setting=self.setting)(wrapper)
        return inner
 