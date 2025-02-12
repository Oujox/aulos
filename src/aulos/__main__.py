import argparse

from aulos.ui import CommandResult, ScaleViewer


def main() -> None:
    parser = argparse.ArgumentParser("aulos")
    parser.description = "Aulos Application"

    subparsers = parser.add_subparsers(dest="command", required=True)
    ScaleViewer(subparsers.add_parser("scale"))

    args = parser.parse_args(namespace=CommandResult)
    args.execute(args())


if __name__ == "__main__":
    main()
