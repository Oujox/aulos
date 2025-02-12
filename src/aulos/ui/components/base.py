import tkinter as tk
import typing as t
from abc import ABCMeta, abstractmethod


class BaseComponent(tk.Frame, metaclass=ABCMeta):
    def __init__(self, master: tk.Misc, **kwargs: t.Any) -> None:
        super().__init__(master, padx=12, pady=4, **kwargs)
        self._callbacks: dict[str, list[t.Callable]] = {}

    @abstractmethod
    def create_widget(self, *args: t.Any, **kwargs: t.Any) -> None:
        return

    @abstractmethod
    def default(self) -> None:
        return

    def bind_callback(self, event_name: str, callback: t.Callable) -> None:
        if event_name not in self._callbacks:
            self._callbacks[event_name] = []
        self._callbacks[event_name].append(callback)

    def unbind_callback(self, event_name: str, callback: t.Callable) -> None:
        if event_name in self._callbacks:
            self._callbacks[event_name].remove(callback)
            if not self._callbacks[event_name]:
                del self._callbacks[event_name]

    def trigger_event(self, event_name: str, *args: t.Any, **kwargs: t.Any) -> t.Callable[[], None]:
        if event_name in self._callbacks:

            def wrapper() -> None:
                for callback in self._callbacks[event_name]:
                    callback(*args, **kwargs)

            return wrapper
        return lambda: None
