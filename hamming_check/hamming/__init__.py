"""
hamming
~~~~~~

hamming package - Various classes for reading and writing data.
"""

__all__ = ["Hamming", "DecodeResult", "DecodeStatus"]

__author__ = "Pablo Alessandro Santos Hugen"
__doc__ = "io package - Various classes for reading and writing data."
# __import__ = ["Bytes", "File"]

from .decode_result import DecodeResult
from .decode_status import DecodeStatus
from .hamming import Hamming
