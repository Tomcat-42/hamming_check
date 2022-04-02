from typing import Iterable
from hamming_check.input.BytesBitIterator import BytesBitIterator

class Bytes(object):
    """
        Abstraction for managing a a Byte and its bits
    """
    def __init__(self, byte: bytes):
        self.__byte = byte
        self.__bits_iterator = BytesBitIterator(self.__byte)

    def __set_iterator(self) -> None:
        self.__bits_iterator = BytesBitIterator(self.__byte)
 
    def set_bytes(self, bytes: bytes) -> None:
        self.__byte = bytes
        self.__set_iterator()

    def get_byte(self) -> bytes:
        return self.__byte

    def get_bits(self) -> Iterable[int]:
        return self.__bits_iterator
