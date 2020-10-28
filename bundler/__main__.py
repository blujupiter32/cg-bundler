# Copyright 2020 Daniel Trowbridge

import argparse

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
