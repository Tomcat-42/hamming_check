from io import BufferedIOBase
from typing import Generator, Iterable

from ._file_byte_iterator import _FileByteIterator


class File(object):
    """
    Abstraction for managing a file and its bytes.
    """

    def __init__(self,
                 file_descriptor: BufferedIOBase,
                 bytes_per_read: int = 1):
        self.__bytes_per_read = bytes_per_read
        self.__file_descriptor = file_descriptor

    def __iter__(self) -> Iterable[int]:
        return _FileByteIterator(self.__file_descriptor, self.__bytes_per_read)

    def write(self, bytes_to_write: bytearray) -> None:
        self.__file_descriptor.write(bytes_to_write)

    def get_bytes(self, number_of_bytes: int) -> Generator[int, int, bytes]:
        for i in range(number_of_bytes):
            yield self.__file_descriptor.read(self.__bytes_per_read)

    def close(self) -> None:
        self.__file_descriptor.close()
        return self
