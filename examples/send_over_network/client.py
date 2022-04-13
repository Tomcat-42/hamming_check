#!/usr/bin/env python

from random import randint, random
import socket
from argparse import ArgumentParser

from hamming_check.hamming import Hamming


def main():
    # argparser
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument("-b", "--bytes", type=int, default=4096)
    parser.add_argument("-d", "--double-noise", action="store_true")
    args = parser.parse_args()

    # opens the socket connection and the file
    s = socket.socket()
    s.connect(("localhost", args.port))
    filetosend = open(args.file, "rb")

    # Hamming check
    hamming = Hamming(args.bytes)
    bytes_to_send = hamming.get_number_of_output_bytes()

    # sends the encoded
    while data := filetosend.read(args.bytes):
        encoded_data = bytearray(hamming.encode(data))
        # 30% chance of sending the data with noise
        if random() > 0.3:
            print("Sending data with noise")
            encoded_data[randint(0, bytes_to_send)] ^= 1 << randint(0, 7)
        # if enabled, 50% of chance to add double noise to data
        if args.double_noise and random() > 0.5:
            print("Sending data with double noise")
            encoded_data[randint(0, bytes_to_send)] ^= 1 << randint(0, 7)
        s.send(encoded_data)

    filetosend.close()
    s.send(b"DONE")
    print("Done Sending.")
    s.shutdown(2)
    s.close()
    exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
