import argparse


def main():
    parser = argparse.ArgumentParser(description="Aulos Application")
    parser.add_argument(
        "--gui", action="store_true", help="run the aulos application in GUI mode"
    )
    args = parser.parse_args()

    if args.gui:
        from aulos.ui import run

        run()


if __name__ == "__main__":
    main()
