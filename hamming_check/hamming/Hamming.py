from enum import Enum
from math import log2

from hamming_check.hamming.DecodeResult import DecodeResult
from hamming_check.hamming.DecodeStatus import DecodeStatus
from hamming_check.input.Bytes import Bytes
from hamming_check.utils.Utils import Utils


class Hamming(object):

    def __init__(self, buffer_size: int = 1):
        """ """
        self.buffer_size = buffer_size
        self.number_of_input_bits = buffer_size * 8

        # k = 0
        # while 2**k - 1 < m + k:
        #     k += 1
        # return k
        self.number_of_parity_bits = int(log2(self.number_of_input_bits) + 1)
        self.number_of_output_bits = (self.number_of_input_bits +
                                      self.number_of_parity_bits + 1)

    def get_syndromes(self, hamming_word: Bytes) -> list[Bytes]:
        """
        Get the syndromes of a hamming word.
        """
        syndromes = [
            Bytes(
                hamming_word.get_bits_if_index(
                    lambda x: (x & 2**i) and not Utils.is_power_of_two(x)),
                endian="little",
            ) for i in range(self.number_of_parity_bits)
        ]

        return syndromes

    def get_parity_bits(self, hamming_word: Bytes) -> list[Bytes]:
        """
        Get the syndromes of a hamming word.
        """
        parity = Bytes(
            hamming_word.get_bits_if_index(
                lambda x: x > 0 and Utils.is_power_of_two(x)),
            endian="little",
        )

        return parity

    def get_data(self, hamming_word: Bytes) -> Bytes:
        """
        Get the data bits from a hamming word.
        """
        return Bytes(
            hamming_word.get_bits_if_index(
                lambda x: x > 0 and not Utils.is_power_of_two(x)),
            endian="little",
        )

    def encode(self, input_bytes: bytes) -> bytes:
        """
        Encode a byte array using the hamming code.
        """

        input_bits = Bytes(buffer=input_bytes, endian="little")
        output_bits = Bytes(endian="little", ).from_size(
            self.number_of_output_bits)

        # copy the m bits to the output
        j = 0
        for i in range(1, self.number_of_output_bits):
            if not Utils.is_power_of_two(i):
                output_bits[i] = input_bits[j]
                j += 1

        # syndrome words for the input bits
        parity_words = self.get_syndromes(output_bits)

        for i in range(self.number_of_parity_bits):
            output_bits[2**i] = parity_words[i].get_parity()

        # calculate the global g parity bit
        output_bits[0] = output_bits.get_parity()

        return output_bits.tobytes()

    def decode(self, hamming_word_bytes) -> DecodeResult:
        """
        Decode a byte array using the hamming code.
        """
        hamming_word = Bytes(endian="little").from_bytes(
            hamming_word_bytes)[:self.number_of_output_bits]

        data_bits = self.get_data(hamming_word)

        # re-hammify the input bits for checking
        hamming_word_prime = Bytes(endian="little").from_bytes(
            self.encode(data_bits.tobytes()))[:self.number_of_output_bits]

        # extract the hamming word syndrome
        hamming_word_parity = self.get_parity_bits(hamming_word)

        # extract the newly generated hamming word syndrome
        hamming_word_prime_parity = Bytes(
            [b.get_parity() for b in self.get_syndromes(hamming_word_prime)],
            endian="little",
        )

        syndrome = ord(
            (hamming_word_parity ^ hamming_word_prime_parity).tobytes())
        global_parity = hamming_word[0] ^ hamming_word_prime[0]

        result = DecodeResult()

        if not syndrome and not global_parity:
            result.set_status(DecodeStatus.NO_ERROR)
        elif syndrome and not global_parity:
            result.set_status(DecodeStatus.SINGLE_ERROR_CORRECTED)
            hamming_word_prime[syndrome] ^= 1
        else:
            result.set_status(DecodeStatus.DOUBLE_ERROR_DETECTED)

        result.set_data(self.get_data(hamming_word_prime).tobytes())

        return result
