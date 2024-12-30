import typing as t
from functools import wraps

from .._core import Setting
from .context import EuterpeContext
from .track import Track


class Euterpe:

    def __init__(self, name: str, *, setting: Setting | None = None):
        self.name = name
        self.setting = setting or Setting.default()

    def WorkSpace(self):
        def inner[**P](func: t.Callable[P, None]) -> t.Callable[P, None]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
                return func(*args, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Track(self):
        """
        A decorator that converts the return value into track data for audio representation.

        Example
        -------

        >>> @workspace.Track()
        ... def track1():
        ...     return []


        """

        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Reverb(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Distortion(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Deray(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Chorus(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Flanger(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Equalizer(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Compressor(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Tremolo(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def PitchShift(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner

    def Looper(self):
        def inner(
            func: t.Callable[t.Concatenate[Track, ...], Track]
        ) -> t.Callable[t.Concatenate[Track, ...], Track]:
            @wraps(func)
            def wrapper(track: Track, **kwargs: ...) -> Track:
                return func(track, **kwargs)

            return EuterpeContext(setting=self.setting)(wrapper)

        return inner
