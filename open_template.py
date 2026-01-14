"""Utility script to open VAVE template files.

This script prints the contents of the supplied file path to stdout. It is a
lightweight helper to quickly inspect any of the provided text templates from
the command line.
"""

from __future__ import annotations

import argparse
import pathlib
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the contents of a VAVE template file."
    )
    parser.add_argument(
        "file",
        type=pathlib.Path,
        help="Path to the template file to open.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding used to read the file (default: utf-8).",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=None,
        help="Optionally limit output to the first N lines.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    file_path = args.file

    if not file_path.exists():
        print(f"Error: {file_path} does not exist.", file=sys.stderr)
        return 1

    if not file_path.is_file():
        print(f"Error: {file_path} is not a file.", file=sys.stderr)
        return 1

    try:
        with file_path.open("r", encoding=args.encoding) as f:
            if args.lines is None:
                sys.stdout.write(f.read())
            else:
                for _ in range(args.lines):
                    line = f.readline()
                    if not line:
                        break
                    sys.stdout.write(line)
    except UnicodeDecodeError as exc:
        print(
            f"Error: Could not decode {file_path} with encoding {args.encoding}: {exc}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
