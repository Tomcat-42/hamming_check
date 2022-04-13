"""
hamming_check.entry_points.py
~~~~~~~~~~~~~~~~~~~~~~

This module contains the entry-point functions for the hamming_check module,
that are referenced in setup.py.
"""

from argparse import ArgumentParser
from sys import argv

from hamming_check.cli import Cli


def cli() -> int:
    """Main package cli entry point.

    Delegates to other functions based on user input.
    """
    cmd_line = Cli()
    result = 0
    try:
        result = cmd_line.run()
    except KeyboardInterrupt:
        print("\nExiting...")

    return result


def flip_a_bit_in_file() -> None:
    """Flip a bit in a file."""
    parser = ArgumentParser(
        description="Flip a bit in a file.",
        epilog="""
        This function is used to flip a bit in a file.
        """,
    )
    parser.add_argument(
        "file",
        help="The file to flip a bit in.",
        type=str,
    )
    parser.add_argument(
        "bit",
        help="The bit to flip.",
        type=int,
    )
    args = parser.parse_args()
    fname = args.file
    bitpos = args.bit
    nbytes, nbits = divmod(bitpos, 8)

    fp = open(fname, "r+b")
    fp.seek(nbytes, 0)
    c = fp.read(1)

    toggled = bytes([ord(c) ^ (1 << nbits)])

    fp.seek(-1, 1)
    fp.write(toggled)
    fp.close()
    print(f"Flipped bit {bitpos} in {fname}")
