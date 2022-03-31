"""
py_pkg.entry_points.py
~~~~~~~~~~~~~~~~~~~~~~

This module contains the entry-point functions for the py_pkg module,
that are referenced in setup.py.
"""

from os import remove
from sys import argv
from zipfile import ZipFile

import requests
from hamming_check.input import FileInput


def main() -> None:
    """Main package entry point.

    Delegates to other functions based on user input.
    """
