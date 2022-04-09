from typing import Generator, Iterator


class _BytesBitIterator(object):
    """
    Iterator over the bits of one or more byte
    """

    def __init__(self, bytes: bytes, endian: str = "big") -> None:
        # endianess of the bytes
        self._endian = endian

        self._bytes = bytes
        # size of the bytestring
        self._size = len(bytes)

        # current byte
        self._byte_index = 0

        # current bit
        self._bit_index = -1 if self._endian == "little" else 8
        self._bit_max_index = 7 if self._endian == "little" else 0
        self._bit_min_index = 0 if self._endian == "little" else 7
        self._bit_step = 1 if self._endian == "little" else -1

    # Iterator implementation,
    # For reading bits on demand
    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if (self._bit_index == self._bit_max_index
                and self._byte_index == self._size - 1):
            raise StopIteration

        if self._bit_index == self._bit_max_index:
            self._bit_index = self._bit_min_index
            self._byte_index += 1
        else:
            self._bit_index += self._bit_step

        self.curr_bit = (self._bytes[self._byte_index] >> self._bit_index) & 1

        return self.curr_bit

    # Generator implementation
    # For reading all the bits in one shot
    # Actually, this should not used, because the iterator is a
    # more efficient approach

    def _get_bits(self) -> Generator[int, None, None]:
        for b in self._bytes:
            for i in range(8):
                yield (b >> i) & 1
