from io import BufferedReader
from typing import Generator, Iterator


class _FileByteIterator(object):
    """
    Reads the file and returns a iterator over the bytes
    """

    def __init__(self,
                 file_descriptor: BufferedReader,
                 bytes_per_read: int = 1):
        self._file_descriptor = file_descriptor
        self._bytes_per_read = bytes_per_read

    def _is_closed(self) -> bool:
        return self._file.closed

    # Iterator implementation,
    # For reading bytes on Demand

    def __iter__(self) -> Iterator[bytes]:
        return self

    def __next__(self) -> bytearray:

        self.byte = self._file_descriptor.read(self._bytes_per_read)
        if self.byte:
            return bytes(self.byte)
        else:
            raise StopIteration

    # Generator implementation
    # For reading all the bytes in one shot
    # Actually, this might be not used, because the iterator is more efficient

    def _get_all_bytes(self,
                       bytes_per_read: int = 1
                       ) -> Generator[bytes, None, None]:

        __curr_byte = 0
        while __curr_byte := self._file.read(bytes_per_read):
            yield bytes(__curr_byte)
