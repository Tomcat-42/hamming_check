from typing import Iterator


class BytesBitIterator(object):
    """
        Iterator over the bits of one or more byte
    """
    def __init__(self, bytes: bytearray):
        self.bytes = bytes
        # size of the bytestring
        self.size = len(bytes)
        # current byte
        self.byte_index = 0
        # current bit
        self.bit_index = -1

    # Iterator implementation,
    # For reading bits on demand
    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.bit_index == 7 and self.byte_index == self.size - 1:
            raise StopIteration

        if self.bit_index == 7:
            self.bit_index = 0
            self.byte_index += 1
        else:
            self.bit_index += 1

        self.curr_bit = (self.bytes[self.byte_index] >> self.bit_index) & 1

        return self.curr_bit

    
    # Generator implementation
    # For reading all the bits in one shot
    # Actually, this should not used, because the iterator is a 
    # more efficient approach
    def __get_bits(self):
        for b in self.bytes:
            for i in range(8):
                yield (b >> i) & 1
