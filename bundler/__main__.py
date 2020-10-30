# Copyright 2020 Daniel Trowbridge
#
# Released under the MIT License (see ../LICENSE)

import argparse
import os


def bundle_file(source_path, separator, dest_file):
    with open(source_path) as source_file:
        for line in source_file:
            if separator in line:
                replacement = line.replace(separator, source_path)
                dest_file.write(replacement)
                break
        else:
            source_file.seek(0)
        dest_file.write(source_file.read())


def source_paths(triple, extension, main):
    for filename in triple[2]:
        if os.path.splitext(filename)[1] == extension:
            path = os.path.join(triple[0], filename)
            if path != main:
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

def main():
    args = parser.parse_args()

    extension = os.path.splitext(args.main)[1]
    paths = (
        path
        for root in args.directories
        for triple in os.walk(root)
        for path in source_paths(triple, extension, args.main)
    )

    with open("bundle" + extension, "w") as dest_file:
        for path in paths:
            bundle_file(path, args.s, dest_file)
            dest_file.write("\n")
        bundle_file(args.main, args.s, dest_file)
        dest_file.flush()

if __name__ == "__main__":
    main()
