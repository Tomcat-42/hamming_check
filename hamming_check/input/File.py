from typing import Iterable
from hamming_check.input.FileByteIterator import FileByteIterator

class File(object):
    """
        Abstraction for managing a file and its bytes.
    """
    def __init__(self, file_name: str, bytes_per_read: int = 1):
        self.__file_name = file_name
        self.__bytes_per_read = bytes_per_read
        self.__bytes_iterator = FileByteIterator(self.__file_name, self.__bytes_per_read)

    def set_bytes_per_read(self, bytes_per_read: int) -> None:
        self.close()
        self.__bytes_iterator = FileByteIterator(self.__file_name, bytes_per_read)

    def get_bytes(self) -> Iterable[bytes]:
        return self.__bytes_iterator

    def close(self) -> None:
        self.__bytes_iterator.close()
