"""
tests.test_io.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the io module
"""
from hamming_check.hamming import DecodeResult, DecodeStatus, Hamming
from hamming_check.io import Bytes, File
from hamming_check.io._bytes_bit_iterator import _BytesBitIterator
from hamming_check.io._file_byte_iterator import _FileByteIterator


class TestBytes:
    """
    Test Suite for the Bytes class
    """

    def test_text_file_generator_single_byte(
            self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        with open(text_file, "rb") as f:
            file_iterator = _FileByteIterator(f)
            bytes_generated = [i for i in file_iterator]

        assert bytes_generated == text_file_single_byte

    def test_text_file_generator_four_bytes(self, text_file: str,
                                            text_file_four_bytes: list[bytes]):
        """Test FileInput class."""

        with open(text_file, "rb") as f:
            bytes_iterator = _FileByteIterator(f, bytes_per_read=4)
            bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_four_bytes

    def test_bytes_bit_iterator_single_byte(self, bytes_single_byte: bytes,
                                            bytes_single_byte_bits: list[int]):
        """Test FileInput class."""

        bits_iterator = _BytesBitIterator(bytes_single_byte)
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_single_byte_bits

    def test_bytes_bit_iterator_three_bytes(self, bytes_three_bytes: bytes,
                                            bytes_three_bytes_bits: list[int]):
        """Test FileInput class."""

        bits_iterator = _BytesBitIterator(bytes_three_bytes)
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_three_bytes_bits

    def test_bytes_bit_iterator_three_bytes_little_endian(
            self, bytes_three_bytes: bytes,
            bytes_three_bytes_bits_little_endian: list[int]):
        """Test FileInput class."""

        bits_iterator = _BytesBitIterator(bytes_three_bytes, endian="little")
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_three_bytes_bits_little_endian
        return True


class TestFile:
    """
    Test Suite for the File class
    """

    def test_file_single_byte(self, text_file: str,
                              text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        with open(text_file, "rb") as f:
            file = File(f, bytes_per_read=1)

            bytes_iterator = file
            bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_single_byte

    def test_file_four_bytes(self, text_file: str,
                             text_file_four_bytes: list[bytes]):
        """Test FileInput class."""
        with open(text_file, "rb") as f:
            file = File(f, bytes_per_read=4)

            bytes_iterator = file
            bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_four_bytes

    def test_bytes(self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        with open(text_file, "rb") as f:
            file = File(f, bytes_per_read=1)

            bytes_iterator = file
            bytes_generated = [i for i in bytes_iterator]

        bytes = Bytes()
        bytes.frombytes(bytes_generated[0])

        assert bytes_generated[0] == bytes.tobytes()
