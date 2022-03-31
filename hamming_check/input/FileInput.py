# from hamming_check.input.GenericInput import GenericInput

# Implementation class for a file reading GenericInput class
class FileInputGenerator():
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.__open()

    def __open(self):
        self.file = open(self.file_name, "rb")

 
    def get_bytes(self, bytes_per_read: int = 1):
        if self.is_closed():
            self.__open()

        __curr_byte = 0
        while(__curr_byte := self.file.read(bytes_per_read)):
            yield __curr_byte

    def get_bits(self, bits_per_read: int = 1):
        bytes = self.get_bytes(bytes_per_read = 1)
        for b in bytes:
            for i in range(8):
                yield (ord(b) >> i) & 1

    def is_closed(self):
            return self.file.closed

    def __close(self):
        self.file.close()
