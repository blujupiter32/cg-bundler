# Copyright 2020 Daniel Trowbridge

import argparse
import os


def source_paths(triple, extension):
    for filename in triple[2]:
        if os.path.splitext(filename)[1] == extension:
            path = os.path.join(triple[0], filename)
            if path != args.main:
                yield path


parser = argparse.ArgumentParser(
    prog="cg-bundler", description="Bundles program files recursively."
)
parser.add_argument(
    "main", help="the main script to be included last", metavar="MAIN"
)
parser.add_argument(
    "directories", help="a root directory to bundle", metavar="DIR", nargs="+"
)
parser.add_argument(
    "-s",
    help='the separator to use (default: "BEGIN CODE")',
    default="BEGIN CODE",
    metavar="SEP",
)

args = parser.parse_args()

extension = os.path.splitext(args.main)[1]
paths = (
    path
    for root in args.directories
    for triple in os.walk(root)
    for path in source_paths(triple, extension)
)
