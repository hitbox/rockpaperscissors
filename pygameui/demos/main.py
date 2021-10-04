import argparse
import sys

from .commandline import climain
from .fitrect import fitrect

SUBCOMMANDS = [climain, fitrect]

def main(argv=None):
    "Run a demo"
    parser = argparse.ArgumentParser(prog=__name__, description=main.__doc__)

    subparsers = parser.add_subparsers()

    for subfunc in SUBCOMMANDS:
        sp = subparsers.add_parser(subfunc.__name__, help=subfunc.__doc__)
        sp.set_defaults(func=subfunc)

    args = parser.parse_args(argv)
    if not hasattr(args, 'func'):
        parser.error('Demo name required.')

    args.func(sys.argv[2:])
