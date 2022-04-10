"""
tests.test_hamming.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the Hamming module.
"""
from hamming_check.hamming import DecodeResult, DecodeStatus, Hamming
from hamming_check.io import Bytes, File


class TestHamming:
    """Test suite for Input module."""

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
