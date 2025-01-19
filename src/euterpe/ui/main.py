
import ctypes
import tkinter as tk
import tkinter.ttk as ttk

from .components import KeyBoard, ScaleViewer


def run():
    # windows only
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = tk.Tk()
    root.title("Euterpe Application GUI")
    root.geometry("1200x800")
    root.resizable(False, False)
    # root.attributes('-topmost', True)
    keyboard = KeyBoard(root)
    keyboard.pack(fill=tk.X)
    scale = ScaleViewer(root)
    scale.pack(fill=tk.X)

    root.mainloop()