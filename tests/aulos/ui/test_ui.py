import tkinter as tk

import pytest

from src.aulos.ui.components import KeyBoard, KeySelecter, ScaleDisplay, ScaleSelecter


@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.quit()


def test_Keyboard_create(root):
    keyboard = KeyBoard(root)
    assert isinstance(keyboard, tk.Misc)
    assert keyboard.winfo_exists()


def test_ScaleDisplay_create(root):
    scaleviewer = ScaleDisplay(root)
    assert isinstance(scaleviewer, tk.Misc)
    assert scaleviewer.winfo_exists()


def test_KeySelecter_create(root):
    keyselecter = KeySelecter(root)
    assert isinstance(keyselecter, tk.Misc)
    assert keyselecter.winfo_exists()


def test_ScaleSelecter_create(root):
    scaleselecter = ScaleSelecter(root)
    assert isinstance(scaleselecter, tk.Misc)
    assert scaleselecter.winfo_exists()
