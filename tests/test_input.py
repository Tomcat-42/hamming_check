"""
tests.test_input.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the Input module that handles everything to do with
Input
"""
from copy import deepcopy

import pytest

from hamming_check.hamming.DecodeResult import DecodeResult
from hamming_check.hamming.DecodeStatus import DecodeStatus
from hamming_check.hamming.Hamming import Hamming
from hamming_check.input.Bytes import Bytes
from hamming_check.input.BytesBitIterator import BytesBitIterator
from hamming_check.input.File import File
from hamming_check.input.FileByteIterator import FileByteIterator


class TestInput:
    """Test suite for Input module."""

    def test_text_file_generator_single_byte(
            self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        bytes_iterator = FileByteIterator(text_file)
        bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_single_byte

    def test_text_file_generator_four_bytes(self, text_file: str,
                                            text_file_four_bytes: list[bytes]):
        """Test FileInput class."""

        bytes_iterator = FileByteIterator(text_file, bytes_per_read=4)
        bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_four_bytes

    def test_bytes_bit_iterator_single_byte(self, bytes_single_byte: bytes,
                                            bytes_single_byte_bits: list[int]):
        """Test FileInput class."""

        bits_iterator = BytesBitIterator(bytes_single_byte)
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_single_byte_bits

    def test_bytes_bit_iterator_three_bytes(self, bytes_three_bytes: bytes,
                                            bytes_three_bytes_bits: list[int]):
        """Test FileInput class."""

        bits_iterator = BytesBitIterator(bytes_three_bytes)
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_three_bytes_bits

    def test_bytes_bit_iterator_three_bytes_little_endian(
            self, bytes_three_bytes: bytes,
            bytes_three_bytes_bits_little_endian: list[int]):
        """Test FileInput class."""

        bits_iterator = BytesBitIterator(bytes_three_bytes, endian="little")
        bits_generated = [i for i in bits_iterator]

        assert bits_generated == bytes_three_bytes_bits_little_endian
        return True

    def test_file_single_byte(self, text_file: str,
                              text_file_single_byte: list[bytes]):
        """Test FileInput class."""
        file = File(text_file)

        bytes_iterator = file.get_bytes()
        bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_single_byte

    def test_file_four_bytes(self, text_file: str,
                             text_file_four_bytes: list[bytes]):
        """Test FileInput class."""

        file = File(text_file, bytes_per_read=4)

        bytes_iterator = file.get_bytes()
        bytes_generated = [i for i in bytes_iterator]

        assert bytes_generated == text_file_four_bytes

    def test_bytes(self, text_file: str, text_file_single_byte: list[bytes]):
        """Test FileInput class."""

        file = File(text_file, bytes_per_read=1)

        bytes_iterator = file.get_bytes()
        bytes_generated = [i for i in bytes_iterator]

        bytes = Bytes()
        bytes.frombytes(bytes_generated[0])

        assert bytes_generated[0] == bytes.tobytes()

    def test_hamming_encode_t(self, t_bytes: bytes, t_hammified: list[int]):
        """Test FileInput class."""
        hamming = Hamming()
        encoded_t = hamming.encode(t_bytes)

        hamming_t = Bytes(endian="little").from_bytes(encoded_t).tolist()

        assert hamming_t == t_hammified

    def test_hamming_encode_t_4flipped(self, t_bytes: bytes,
                                       t_hammified_bit4_flipped: list[int]):
        """Test FileInput class."""
        hamming = Hamming()
        encoded_t = hamming.encode(t_bytes)

        hamming_t = Bytes(endian="little").from_bytes(encoded_t).tolist()

        assert hamming_t != t_hammified_bit4_flipped

    def test_hamming_decode_t_no_error(self, t_bytes: bytes,
                                       t_hammified: list[int]):
        """Test FileInput class."""

        hamming = Hamming()
        encoded_t = hamming.encode(t_bytes)

        decoded_t = hamming.decode(encoded_t)

        assert (decoded_t.get_status() == DecodeStatus.NO_ERROR
                and decoded_t.get_data() == t_bytes)

    def test_hamming_decode_t_sec(self, t_bytes: bytes,
                                  t_hammified_bit4_flipped: list[int]):
        """Test FileInput class."""

        hamming = Hamming()
        encoded_t = Bytes(t_hammified_bit4_flipped, endian="little").tobytes()

        decoded_t = hamming.decode(encoded_t)

        assert (decoded_t.get_status() == DecodeStatus.SINGLE_ERROR_CORRECTED
                and decoded_t.get_data() == t_bytes)

    def test_hamming_decode_t_dec(self, t_bytes,
                                  t_hammified_bit4_bit11_flipped: list[int]):
        """Test FileInput class."""

        hamming = Hamming()
        encoded_t = Bytes(t_hammified_bit4_bit11_flipped,
                          endian="little").tobytes()

        decoded_t = hamming.decode(encoded_t)

        assert (decoded_t.get_status() == DecodeStatus.DOUBLE_ERROR_DETECTED
                and decoded_t.get_data() != t_bytes)
