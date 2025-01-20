import tkinter as tk

import pytest

from src.aulos.ui import KeyBoard, ScaleViewer


@pytest.fixture(scope="function")
def root():
    root = tk.Tk()
    yield root
    root.quit()


def test_Keyboard_create(root):
    keyboard = KeyBoard(root)
    assert isinstance(keyboard, tk.Misc)
    assert keyboard.winfo_exists()


def test_ScaleViewer_create(root):
    scaleviewer = ScaleViewer(root)
    assert isinstance(scaleviewer, tk.Misc)
    assert scaleviewer.winfo_exists()
