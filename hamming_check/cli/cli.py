import builtins as exceptions
from argparse import ArgumentParser, FileType
from copy import Error
from sys import stderr, stdin, stdout

from hamming_check.hamming import DecodeResult, DecodeStatus, Hamming
from hamming_check.io import File
from hamming_check.types import VerbosityTypes


class Cli(object):
    """
    This class is used to perform the command line operations.
    """

    def __init__(self):
        """
        Initialize the command line interface and parse the arguments.
        """
        self.parser = ArgumentParser()
        self.args = None
        self._parse_args()

    def _parse_args(self) -> None:

        self.parser.add_argument(
            "input_file",
            nargs="?",
            type=FileType("rb"),
            default=stdin.buffer,
            help="file used for reading data. If not specified, "
            "data is read from stdin.",
        )

        self.parser.add_argument(
            "output_file",
            nargs="?",
            type=FileType("wb"),
            default=stdout.buffer,
            help="file used for writing data. If not specified, "
            "data is written to stdout.",
        )

        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-e",
            "--encode",
            action="store_true",
            help="encode a file into a hamming-encoded file",
        )
        group.add_argument(
            "-d",
            "--decode",
            action="store_true",
            help="decode a hamming-encoded file into a file",
        )

        self.parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="increase output verbosity (can be used multiple times)",
        )

        self.parser.add_argument(
            "-b",
            "--buffer-size",
            type=int,
            default=1,
            help="change the buffer size (in bytes) used for encoding/decoding",
        )

        self.args = self.parser.parse_args()
        self.hamming = Hamming(self.args.buffer_size, self.args.verbose)
        self.number_of_output_bytes = self.hamming.get_number_of_output_bytes()

    def run(self) -> int:
        """
        Run the command line interface.
        :return: int.
        """
        return self.decode() if self.args.decode else self.encode()

    def encode(self) -> None:
        """
        Encode the input stream to the output stream.
        :return: None.
        """
        exit_value = 0

        input_file = File(self.args.input_file, self.args.buffer_size)
        output_file = File(self.args.output_file)

        try:
            for (index, data) in enumerate(input_file):
                encoded_data = self.hamming.encode(data)
                if self.args.verbose >= VerbosityTypes.DECODE_ENCODE_RESULTS:
                    print(f"{index}: Encoded {data} -> {encoded_data}")
                output_file.write(encoded_data)
        except KeyboardInterrupt as e:
            print(f"\n\nBye!")
        except FileReadError as e:
            stderr.write(f"Error Reading file!\n")
            exit_value = 1
        except FileWriteError as e:
            stderr.write(f"Error Writing file!\n")
            exit_value = 1
        except KeyboardInterrupt:
            print("\nInterrupted by user, bye!")
        except Error:
            stderr.write(f"Error encoding data!\nCheck the --buffer-size "
                         f"option and the i/o files!\n")
            exit_value = 1
        finally:
            self.args.input_file.close()
            self.args.output_file.close()

        return exit_value

    def decode(self) -> None:
        """
        Decode the input stream to the output stream.
        :return: None.
        """
        exit_value = 0
        try:
            input_file = File(self.args.input_file,
                              self.number_of_output_bytes)
            output_file = File(self.args.output_file)

            for (index, data) in enumerate(input_file):
                decoded_result = self.hamming.decode(data)
                decoded_data, decoded_result = (
                    decoded_result.get_data(),
                    decoded_result.get_status(),
                )

                if self.args.verbose >= VerbosityTypes.DECODE_ENCODE_RESULTS:
                    print(f"{index}: Decoded {data} -> {decoded_data}",
                          end=", ")
                    if decoded_result == DecodeStatus.NO_ERROR:
                        print("No Errors Detected")
                    elif decoded_result == DecodeStatus.SINGLE_ERROR_CORRECTED:
                        print("Single Error Corrected")
                if (self.args.verbose >= VerbosityTypes.ONLY_ERRORS and
                        decoded_result == DecodeStatus.DOUBLE_ERROR_DETECTED):
                    print(f"{index}: Decoded {data} -> {decoded_data}, "
                          f"Double Error Detected")
                    exit_value = 2

                output_file.write(decoded_data)
        except Error:
            stderr.write(f"Error decoding data!\nCheck the --buffer-size "
                         f"option and the i/o files!\n")
            exit_value = 1
        finally:
            self.args.input_file.close()
            self.args.output_file.close()

        return exit_value
