"""
hamming check
~~~~~~

The hamming check package - a project that is intended
to be used as a library and command line tool for checking
file integrity using the hamming code.
"""

__all__ = ["Hamming", "DecodeResult", "DecodeStatus", "File", "Bytes"]

__author__ = "Pablo Alessandro Santos Hugen"
__doc__ = "io package - Various classes for reading and writing data."
# __import__ = ["Bytes", "File"]

from .hamming import DecodeResult, DecodeStatus, Hamming
from .io import Bytes, File
