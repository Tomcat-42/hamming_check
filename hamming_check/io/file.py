from typing import Generator, Iterable

from ._file_byte_iterator import _FileByteIterator


class File(object):
    """
    Abstraction for managing a file and its bytes.
    """

    def __init__(self,
                 file_name: str,
                 bytes_per_read: int = 1,
                 mode: str = "rb"):
        self.__file_name = file_name
        self.__bytes_per_read = bytes_per_read
        self.__file_descriptor = None
        self.__mode = mode

    def open(self, mode: str = "rb") -> None:
        self.__file_descriptor = open(self.__file_name, mode)
        return self

    def __iter__(self) -> Iterable[int]:
        return _FileByteIterator(self.__file_name, self.__bytes_per_read)

    def get_bytes(self, number_of_bytes: int) -> Generator[int, int, bytes]:
        self.open("rb")
        for i in range(number_of_bytes):
            yield self.__file_descriptor.read(self.__bytes_per_read)
        self.close()

    def close(self) -> None:
        self.__file_descriptor.close()
        return self
