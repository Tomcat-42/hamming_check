from enum import Enum
from math import log2

from hamming_check.hamming import DecodeResult, DecodeStatus
from hamming_check.io import Bytes
from hamming_check.types.verbosity_types import VerbosityTypes
from hamming_check.utils import Utils


class Hamming(object):

    def __init__(self, buffer_size: int = 1, verbose: VerbosityTypes = 0):
        self.buffer_size = buffer_size
        self.verbose = verbose

        self.number_of_input_bits = buffer_size * 8

        # k = 0
        # while 2**k - 1 < m + k:
        #     k += 1
        # return k
        self.number_of_parity_bits = int(log2(self.number_of_input_bits) + 1)
        self.number_of_output_bits = (self.number_of_input_bits +
                                      self.number_of_parity_bits + 1)
        self.number_of_output_bytes = round((self.number_of_output_bits) / 8)

    def set_verbosity(self, verbosity: VerbosityTypes):
        """
        Set the verbosity of the hamming code.
        """
        self.verbose = verbosity

    def get_number_of_output_bytes(self) -> int:
        """
        Get the number of input bits.
        """
        return self.number_of_output_bytes

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

        input_bits = (Bytes(
            endian="little").from_bytes(input_bytes).pad_to_size(
                self.number_of_input_bits))
        output_bits = Bytes(endian="little", ).from_size(
            self.number_of_output_bits)

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\n\tEncoding {input_bytes} -> {input_bits}")

        # copy the m bits to the output
        j = 0
        for i in range(1, self.number_of_output_bits):
            if not Utils.is_power_of_two(i):
                output_bits[i] = input_bits[j]
                j += 1

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\tCopied the M bits to the output hamming word -> {output_bits}"
            )

        # syndrome words for the input bits
        parity_words = self.get_syndromes(output_bits)

        for i in range(self.number_of_parity_bits):
            output_bits[2**i] = parity_words[i].get_parity()

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\tExtracted the parity words from the M bits: ")
            for i, word in enumerate(parity_words):
                print(f"\t\tC{2**i} -> {word} -> {word.get_parity()}")

        # calculate the global g parity bit
        output_bits[0] = output_bits.get_parity()

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\tCalculated the global parity bit -> {output_bits[0]}")

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\tHamming word generated -> {output_bits}")

        return output_bits.tobytes()

    def decode(self, hamming_word_bytes) -> DecodeResult:
        """
        Decode a byte array using the hamming code.
        """
        hamming_word = Bytes(endian="little").from_bytes(
            hamming_word_bytes)[:self.number_of_output_bits]

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\n\tDecoding {hamming_word_bytes} -> {hamming_word}")

        data_bits = self.get_data(hamming_word)

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\tExtracted the M bits from the hamming word-> {data_bits}")

        old_verbose = self.verbose
        self.set_verbosity(VerbosityTypes.QUIET)
        # re-hammify the input bits for checking
        hamming_word_prime = Bytes(endian="little").from_bytes(
            self.encode(data_bits.tobytes()))[:self.number_of_output_bits]
        self.set_verbosity(old_verbose)

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\tRe-hammified the input bits for checking -> {hamming_word_prime}"
            )

        # extract the hamming word syndrome
        hamming_word_parity = self.get_parity_bits(hamming_word)

        # extract the newly generated hamming word syndrome
        hamming_word_prime_parity = Bytes(
            [b.get_parity() for b in self.get_syndromes(hamming_word_prime)],
            endian="little",
        )

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\tExtracted the parity bits from the hamming word -> {hamming_word_parity}"
            )
            print(
                f"\tExtracted the parity bits from the re-hammified word -> {hamming_word_parity}"
            )

        syndrome_bits = hamming_word_parity ^ hamming_word_prime_parity
        syndrome = ord(syndrome_bits.tobytes())

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\tCalculated the syndrome word -> {hamming_word_parity } ^ {hamming_word_prime_parity} -> {syndrome_bits} -> {syndrome}"
            )

        global_parity = hamming_word[0] ^ hamming_word_prime[0]

        if self.verbose >= VerbosityTypes.HAMMING_STEPS:
            print("\tExtracted the parity bit from the hamming word ->",
                  hamming_word[0])
            print(
                "\tExtracted the parity bit from the re-hammified word ->",
                hamming_word_prime[0],
            )
            print(
                f"\tCalculated the global parity bit -> {hamming_word[0]} ^ {hamming_word_prime[0]} -> {global_parity}"
            )

        result = DecodeResult()

        if not syndrome and not global_parity:
            result.set_status(DecodeStatus.NO_ERROR)
            if self.verbose >= VerbosityTypes.HAMMING_STEPS:
                print("\tG = {0} and syndrome = {0} -> No error detected")
        elif syndrome and not global_parity:
            result.set_status(DecodeStatus.SINGLE_ERROR_CORRECTED)
            hamming_word_prime[syndrome] ^= 1
            if self.verbose >= VerbosityTypes.HAMMING_STEPS:
                print(
                    f"\tG = 0 and Syndrome = {syndrome} -> Corrected the single error on index {syndrome} -> {hamming_word_prime}"
                )
        else:
            result.set_status(DecodeStatus.DOUBLE_ERROR_DETECTED)
            if self.verbose >= VerbosityTypes.HAMMING_STEPS:
                print(
                    f"\tG = 1 -> Double error detected -> {hamming_word_prime}"
                )

        result.set_data(self.get_data(hamming_word_prime).tobytes())

        return result
