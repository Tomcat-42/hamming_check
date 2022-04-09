from io import BufferedReader
from typing import Generator, Iterator


class FileByteIterator(object):
    """
        Reads the file and returns a iterator over the bytes
    """
    def __init__(self, file_name: str, bytes_per_read: int = 1):
        self.file_name = file_name
        self.bytes_per_read = bytes_per_read
        self.__open()

    def __open(self) -> BufferedReader:
        self.file = open(self.file_name, "rb")
        return self.file

    def __is_closed(self):
        return self.file.closed

    def close(self) -> None:
        self.file.close()

    
    # Iterator implementation,
    # For reading bytes on Demand
    def __iter__(self) -> Iterator[bytes]:
        return self

    def __next__(self) -> bytes:
        if self.__is_closed():
            self.__open()

        self.byte = self.file.read(self.bytes_per_read)
        if self.byte:
            return bytes(self.byte)
        else:
            self.close()
            raise StopIteration

    
    # Generator implementation
    # For reading all the bytes in one shot
    # Actually, this might be not used, because the iterator is more efficient
    def __get_all_bytes(self, bytes_per_read: int = 1) -> Generator[bytes, None, None]:
        if self.__is_closed():
            self.__open()

        __curr_byte = 0
        while(__curr_byte := self.file.read(bytes_per_read)):
            yield bytes(__curr_byte)
