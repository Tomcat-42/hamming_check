from __future__ import annotations

from typing import Any, Callable, Iterable, Union

from bitarray import bitarray
from bitarray.util import parity, zeros

from ._bytes_bit_iterator import _BytesBitIterator


class Bytes(bitarray):
    """
    Abstraction for managing a Byte and its bits
    based on the bitarray class
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init_subclass__().__init__(*args, **kwargs)

    def from_size(self, size: int = 0) -> Bytes:
        """
        Create a Bytes object of a given size
        """
        self.clear()
        self.extend(zeros(size))
        return self

    def from_bytes(self, bytes: bytes) -> Bytes:
        """
        Create a Bytes object from a bytes object
        """
        self.clear()
        self.frombytes(bytes)
        return self

    def get_bits_if_index(self, f_x: Callable[[int], bool]) -> Bytes:
        """
        Return a Bytes object with only the bits that his index satisfy the predicate
        """
        return Bytes([self[i] for i in range(len(self)) if f_x(i)])

    def set_bits_if_index(self,
                          f_x: Callable[[int], int],
                          value: int = 1) -> Bytes:
        """
        Set the bits that his index satisfy the predicate
        """
        for i in range(len(self)):
            if f_x(i):
                self[i] = value

        return self

    def flip_bits_if_index(self, f_x: Callable[[int], int]) -> Bytes:
        """
        Flip the bits that his index satisfy the predicate
        """
        for i in range(len(self)):
            if f_x(i):
                self[1] ^= 1

        return self

    def get_parity(self) -> int:
        """
        Return the parity of the Bytes object
        """
        return parity(self)

    def get_bits(self) -> Iterable[int]:
        return _BytesBitIterator(self.tobytes(), endian=self.endian())

    def pad_to_size(self, size: int) -> Bytes:
        """
        Pad the Bytes object to a given size
        """
        self.extend(zeros(size - len(self)))
        return self

    def __str__(self) -> str:
        return self.to01()
