"""
tests.test_input.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the Input module that handles everything to do with
Input
"""
from copy import deepcopy
import pytest

from hamming_check.input.FileByteIterator import FileByteIterator
from hamming_check.input.BytesBitIterator import BytesBitIterator

from hamming_check.input.File import File
from hamming_check.input.Bytes import Bytes
 
class TestInput:
    """Test suite for Input module."""

    def test_text_file_generator_single_byte(self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        bytes_iterator = FileByteIterator(text_file)
        bytes_generated = [ i for i in bytes_iterator ]

        assert bytes_generated == text_file_single_byte

    def test_text_file_generator_four_bytes(self, text_file: str, text_file_four_bytes: list[bytes]):
        """Test FileInput class."""

        bytes_iterator = FileByteIterator(text_file, bytes_per_read=4)
        bytes_generated = [ i for i in bytes_iterator ]


        assert bytes_generated == text_file_four_bytes

    def test_bytes_bit_iterator_single_byte(self, bytes_single_byte: bytes, bytes_single_byte_bits: list[int]):
        """Test FileInput class."""


        bits_iterator = BytesBitIterator(bytes_single_byte)
        bits_generated = [ i for i in bits_iterator ]

        assert bits_generated == bytes_single_byte_bits

    def test_bytes_bit_iterator_three_bytes(self, bytes_three_bytes: bytes, bytes_three_bytes_bits: list[int]):
        """Test FileInput class."""


        bits_iterator = BytesBitIterator(bytes_three_bytes)
        bits_generated = [ i for i in bits_iterator ]

        assert bits_generated == bytes_three_bytes_bits

    def test_file_single_byte(self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""
        file = File(text_file)

        bytes_iterator = file.get_bytes()
        bytes_generated = [ i for i in bytes_iterator ]

        assert bytes_generated == text_file_single_byte

    def test_file_four_bytes(self, text_file: str, text_file_four_bytes: list[bytes]):
        """Test FileInput class."""

        file = File(text_file, bytes_per_read=4)

        bytes_iterator = file.get_bytes()
        bytes_generated = [ i for i in bytes_iterator ]


        assert bytes_generated == text_file_four_bytes
