# Copyright 2020, 2023 Daniel Trowbridge
#
# Released under the MIT License (see ../LICENSE)

import argparse
import os
import typing


def bundle_file(
    source_path: str, separator: str, dest_file: typing.TextIO
) -> None:
    """Write the contents of `source_path` into `dest_file`.

    If `separator` is encountered in the source file, it is replaced with
    `source_path` and all preceding lines are omitted in `dest_file`.
    Otherwise, the entire file is copied.
    """
    with open(source_path, encoding="utf8") as source_file:
        for line in source_file:
            if separator in line:
                replacement = line.replace(separator, source_path)
                dest_file.write(replacement)
                break
        else:
            source_file.seek(0)
        dest_file.write(source_file.read())


def get_source_paths(
    triple: (typing.Any, typing.Any, typing.Iterable[str]),
    extension: str,
    main_path: str,
) -> typing.Generator[str, None, None]:
    """Extract paths to source files from a triple returned by `os.walk`.

    Only files with the given `extension` are yielded by the generator. If
    `main_path` is encountered, it is skipped.
    """
    for filename in triple[2]:
        if os.path.splitext(filename)[1] == extension:
            path = os.path.join(triple[0], filename)
            if path != main_path:
                yield path


def create_parser() -> argparse.ArgumentParser:
    """Create and return a parser for command line arguments."""
    parser = argparse.ArgumentParser(
        prog="cg-bundler", description="Bundles program files recursively."
    )
    parser.add_argument(
        "main", help="the main script to be included last", metavar="MAIN"
    )
    parser.add_argument(
        "directories",
        help="a root directory to bundle",
        metavar="DIR",
        nargs="+",
    )
    parser.add_argument(
        "-s",
        help='the separator to use (default: "BEGIN CODE")',
        default="BEGIN CODE",
        metavar="SEP",
    )
    return parser


def main() -> None:
    """Bundle source files as indicated by the command line arguments."""
    args = create_parser().parse_args()

    extension = os.path.splitext(args.main)[1]
    paths = (
        path
        for root in args.directories
        for triple in os.walk(root)
        for path in get_source_paths(triple, extension, args.main)
    )

    with open("bundle" + extension, "w", encoding="utf8") as dest_file:
        for path in paths:
            bundle_file(path, args.s, dest_file)
            dest_file.write("\n")
        bundle_file(args.main, args.s, dest_file)
        dest_file.flush()


if __name__ == "__main__":
    main()
