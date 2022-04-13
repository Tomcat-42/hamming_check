#!/usr/bin/env python
import socket
from argparse import ArgumentParser

from hamming_check.hamming import DecodeResult, DecodeStatus, Hamming
from hamming_check.types.verbosity_types import VerbosityTypes


def main() -> None:
    # ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-b", "--bytes", type=int, default=4096)
    args = parser.parse_args()

    # opens socket
    s = socket.socket()
    s.bind(("localhost", args.port))
    s.listen(1)
    c, a = s.accept()
    filetodown = open(args.file, "wb")

    # Hamming check
    hamming = Hamming(args.bytes, VerbosityTypes.QUIET)
    bytes_to_receive = hamming.get_number_of_output_bytes()

    while True:
        data = c.recv(bytes_to_receive, socket.MSG_WAITALL)

        if data == b"DONE" or len(data) == 0:
            print("Done Receiving.")
            break

        encoded_data = hamming.decode(data)

        # if status is not DecodeStatus.NO_ERROR or
        # DecodeStatus.SINGLE_ERROR_CORRECTED, then we have a problem
        bytes_received, status = encoded_data.get_data(
        ), encoded_data.get_status()

        if status == DecodeStatus.SINGLE_ERROR_CORRECTED:
            print("One error detected, and corrected")
        elif status == DecodeStatus.DOUBLE_ERROR_DETECTED:
            print("Two errors detected, your file is corrupted")

        filetodown.write(bytes_received)
        filetodown.flush()

    filetodown.close()
    c.shutdown(2)
    c.close()
    s.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
