import argparse


def main():
    parser = argparse.ArgumentParser(description="Euterpe Application")
    parser.add_argument(
        "--gui", action="store_true", help="run the euterpe application in GUI mode"
    )
    args = parser.parse_args()

    if args.gui:
        from euterpe.ui import run

        run()


if __name__ == "__main__":
    main()
