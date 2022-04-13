from enum import Enum
from math import ceil, log2
from typing import List

from hamming_check.hamming import DecodeResult, DecodeStatus
from hamming_check.io import Bytes
from hamming_check.types.verbosity_types import VerbosityTypes
from hamming_check.utils import Utils


class Hamming(object):

    def __init__(self, buffer_size: int = 1, verbose: VerbosityTypes = 0):
        self._buffer_size = buffer_size
        self._verbose = verbose

        self._number_of_input_bits = buffer_size * 8

        # k = 0
        # while 2**k - 1 < m + k:
        #     k += 1
        self._number_of_parity_bits = int(log2(self._number_of_input_bits) + 1)
        self._number_of_output_bits = (self._number_of_input_bits +
                                       self._number_of_parity_bits + 1)
        self._number_of_output_bytes = ceil((self._number_of_output_bits) / 8)

        # pre calculate the syndromes bits index, parity bits indexes
        # and data bit indexes
        self._syndrome_bits_indexes = [[
            j for j in range(3, self._number_of_output_bits)
            if (j & (2**i)) and not Utils.is_power_of_two(j)
        ] for i in range(self._number_of_parity_bits)]
        self._parity_bits_indexes = [
            2**i for i in range(self._number_of_parity_bits)
        ]
        self._data_bits_indexes = [
            j for j in range(self._number_of_output_bits)
            if j and not Utils.is_power_of_two(j)
        ]

    def set_verbosity(self, verbosity: VerbosityTypes):
        """
        Set the verbosity of the hamming code.
        """
        setattr(self, "_verbose", verbosity)
        return self

    def get_verbosity(self):
        """
        Set the verbosity of the hamming code.
        """
        return getattr(self, "_verbose")

    def get_number_of_output_bytes(self) -> int:
        """
        Get the number of input bits.
        """
        return self._number_of_output_bytes

    def _get_syndromes(self, hamming_word: Bytes) -> List[Bytes]:
        """
        Get the syndromes of a hamming word.
        """
        return [
            Bytes(
                (hamming_word[j] for j in self._syndrome_bits_indexes[i]),
                endian="little",
            ) for i in range(self._number_of_parity_bits)
        ]

    def _get_parity_bits(self, hamming_word: Bytes) -> List[Bytes]:
        """
        Get the syndromes of a hamming word.
        """
        return Bytes((hamming_word[i] for i in self._parity_bits_indexes),
                     endian="little")

    def get_data(self, hamming_word: Bytes) -> Bytes:
        """
        Get the data bits from a hamming word.
        """
        return Bytes((hamming_word[i] for i in self._data_bits_indexes),
                     endian="little")

    def encode(self, input_bytes: bytes) -> bytes:
        """
        Encode a byte array using the hamming code.
        """

        input_bits = (Bytes(
            endian="little").from_bytes(input_bytes).pad_to_size(
                self._number_of_input_bits))

        output_bits = Bytes(endian="little", ).from_size(
            self._number_of_output_bits)

        # copy the m bits to the output
        j = 0
        for i in range(1, self._number_of_output_bits):
            if not Utils.is_power_of_two(i):
                output_bits[i] = input_bits[j]
                j += 1

        if self._verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\n\tEncoding {input_bytes} -> {input_bits}\n",
                f"\tCopied the M bits to the output hamming word -> {output_bits}",
            )

        # syndrome words for the input bits
        parity_words = self._get_syndromes(output_bits)

        for i in range(self._number_of_parity_bits):
            output_bits[2**i] = parity_words[i].get_parity()

        # calculate the global g parity bit
        output_bits[0] = output_bits.get_parity()

        if self._verbose >= VerbosityTypes.HAMMING_STEPS:
            print("\tExtracted the parity words from the M bits: ")
            for i, word in enumerate(parity_words):
                print(f"\t\tC{2**i} -> {word} -> {word.get_parity()}")
            print(f"\tCalculated the global parity bit -> {output_bits[0]}\n"
                  f"\tHamming word generated -> {output_bits}")

        return output_bits.tobytes()

    def decode(self, hamming_word_bytes) -> DecodeResult:
        """
        Decode a byte array using the hamming code.
        """

        hamming_word = (Bytes(
            endian="little").from_bytes(hamming_word_bytes).pad_to_size(
                self._number_of_output_bytes *
                8)[:self._number_of_output_bits])
        data_bits = self.get_data(hamming_word)

        old_verbose = self.get_verbosity()
        self.set_verbosity(VerbosityTypes.QUIET)

        # re-hammify the input bits for checking
        hamming_word_prime = Bytes(endian="little").from_bytes(
            self.encode(data_bits.tobytes()))[:self._number_of_output_bits]

        self.set_verbosity(old_verbose)

        # extract the hamming word syndrome
        hamming_word_parity = self._get_parity_bits(hamming_word)

        # extract the newly generated hamming word syndrome
        hamming_word_prime_parity = Bytes(
            [b.get_parity() for b in self._get_syndromes(hamming_word_prime)],
            endian="little",
        )

        syndrome_bits = hamming_word_parity ^ hamming_word_prime_parity
        syndrome = int.from_bytes(syndrome_bits.tobytes(), byteorder="little")

        if self._verbose >= VerbosityTypes.HAMMING_STEPS:
            print(
                f"\n\tDecoding {hamming_word_bytes} -> {hamming_word}\n",
                f"\tExtracted the M bits from the hamming word-> {data_bits}\n"
                f"\tRe-hammified the input bits for checking -> {hamming_word_prime}\n"
                f"\tExtracted the parity bits from the hamming word -> {hamming_word_parity}\n"
                f"\tExtracted the parity bits from the re-hammified word -> {hamming_word_prime_parity}\n"
                f"\tCalculated the syndrome word -> {hamming_word_parity } ^ {hamming_word_prime_parity} -> {syndrome_bits} -> {syndrome}",
            )

        result = DecodeResult()

        if not syndrome:
            result.set_status(DecodeStatus.NO_ERROR)
            if self._verbose >= VerbosityTypes.HAMMING_STEPS:
                print("\tsyndrome = 0 -> No error detected")
        elif syndrome <= self._number_of_output_bits:
            result.set_status(DecodeStatus.SINGLE_ERROR_CORRECTED)
            hamming_word_prime[syndrome] ^= 1
            if self._verbose >= VerbosityTypes.HAMMING_STEPS:
                print(
                    f"\tSyndrome = {syndrome} -> Corrected the single error on index {syndrome} -> {hamming_word_prime}"
                )

        g = hamming_word.get_parity()
        g_prime = hamming_word_prime.get_parity()

        if self._verbose >= VerbosityTypes.HAMMING_STEPS:
            print(f"\tCalculated the new G' parity bit -> {g_prime}")

        if g ^ g_prime:
            result.set_status(DecodeStatus.DOUBLE_ERROR_DETECTED)
            if self._verbose >= VerbosityTypes.HAMMING_STEPS:
                print(f"\tG = {g} != G' = {g_prime} -> Double error detected")
        else:
            if self._verbose >= VerbosityTypes.HAMMING_STEPS:
                print(
                    f"\tG = {g} == G' = {g_prime} -> The hamming word is correct"
                )

        return result.set_data(self.get_data(hamming_word_prime).tobytes())
