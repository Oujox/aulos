def run_gui() -> None:
    import ctypes
    import tkinter as tk

    from aulos.ui import KeyBoard, ScaleViewer

    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = tk.Tk()
    root.title("Aulos Application GUI")
    root.geometry("1200x800")
    root.resizable(width=False, height=False)
    keyboard = KeyBoard(root)
    keyboard.pack(fill=tk.X)
    scale = ScaleViewer(root)
    scale.pack(fill=tk.X)

    root.mainloop()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Aulos Application")
    parser.add_argument(
        "-gui",
        action="store_true",
        help="run the aulos application in GUI mode",
    )
    args = parser.parse_args()

    if args.gui:
        run_gui()


if __name__ == "__main__":
    main()
