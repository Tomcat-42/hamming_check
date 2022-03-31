"""
tests.test_input.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the Input module that handles everything to do with
Input
"""
from copy import deepcopy
import pytest

from hamming_check.input.FileInput import FileInputGenerator

class TestInput:
    """Test suite for Input class."""

    def test_text_file_generator_byte_single(self, text_file: str):
        """Test FileInput class."""

        bytes_generator = FileInputGenerator(text_file)
        bytes_generated = [ i for i in bytes_generator.get_bytes() ]

        assert bytes_generated == [b't', b'e', b's', b't', b'e', b'\n']

    def test_text_file_generator_byte_double(self, text_file: str):
        """Test FileInput class."""
        bytes_generator = FileInputGenerator(text_file)
        bytes_generated = [ i for i in bytes_generator.get_bytes(2) ]
       
        assert bytes_generated == [b'te', b'st', b'e\n']

    def test_bin_file_generator_byte(self, bin_file: str):
        """Test FileInput class."""
      
        bytes_generator = FileInputGenerator(bin_file)
        bytes_generated = [ i for i in bytes_generator.get_bytes(1) ]
       
        assert bytes_generated == [b'a', b'\n']

    def test_bin_file_generator_bit(self, bin_file: str):
        """Test FileInput class."""
        bits_generator = FileInputGenerator(bin_file)
        bits_generated = [ i for i in bits_generator.get_bits() ]
      
        assert bits_generated == [ 1, 0, 0, 0, 0, 1, 1, 0,
                                   0, 1, 0, 1, 0, 0, 0, 0 ]
        return True
