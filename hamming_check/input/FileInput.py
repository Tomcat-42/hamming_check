from hamming_check.input import GenericInput

# Implementation class fro a file reading GenericInput class
class FileInput(GenericInput):
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(self.file_name, 'rb')
    
    def get_bytes(self):
        while 1:
            byte_s = self.file.read(1)
            if not byte_s:
                self.file.close()
                break
            byte = byte_s[0]
            print(byte)

