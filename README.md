# hamming-check

A command line tool and python library to encode and decode data using a generic (in byte size) hamming code algorithm.

## Hamming Code

Hamming code is a set of error-correction codes that can be used to detect and correct the errors that can occur when the data
is moved or stored from the sender to the receiver. It is technique developed by R.W. Hamming for error correction.

You can find more about it on his [Wikipedia Article](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjvkdeftJD3AhV_rpUCHRZBCS4QFnoECBIQAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FHamming_code&usg=AOvVaw1bgDIw5XksNiMYziP2VeeQ), [MSU notes](https://users.math.msu.edu/users/halljo/classes/codenotes/Hamming.pdf) and in the awesome videos by [3Blue1Brown](https://www.youtube.com/c/3blue1brown): [Hamming pt1](https://www.youtube.com/watch?v=X8jsijhllIA) and [Hamming pt2](https://www.youtube.com/watch?v=b3NxrZOu_CE).

## Command Line Interface

### Description

`hamming_check` is a cli tool that is intended to help creating secure copies of a file in a hamming encoded output file, and fixing that secure file for single bit corruptions. Also it can check for double bit corruptions, but could not fix that type of error.

### Usage

```
usage: hamming_check [-h] (-e | -d) [-v] [-b BUFFER_SIZE]
                     [input_file] [output_file]

positional arguments:
  input_file            file used for reading data. If not specified,
                        data is read from stdin.
  output_file           file used for writing data. If not specified,
                        data is written to stdout.

options:
  -h, --help            show this help message and exit
  -e, --encode          encode a file into a hamming-encoded file
  -d, --decode          decode a hamming-encoded file into a file
  -v, --verbose         increase output verbosity (can be used
                        multiple times)
  -b BUFFER_SIZE, --buffer-size BUFFER_SIZE
                        change the buffer size (in bytes) used for
                        encoding/decoding
```

- **input_file**: original file that will be secure copied or a secure file that will be recovered. _If not provided, data will be read from STDIN_.
- **output_file**: secure file that will be created from a file or a file that will be recovered from a secure file. _If not provided, data will be written to STDOUT_.
- **-e|--encode**: Sets the encoding operation. _File_ -> _Secure File_.
- **-d|--decode**: Sets the decoding operation. _Secure File_ -> _File_ with error checking/correction.
- **-b|--buffer-size**: Sets the number of bytes that will be used for the hamming code, default is 1. Higher Values tends to speed up encoding.
- **-v**: Sets the verbosity. If not provided, will be in quiet mode, if `-v`, only errors will be printed, `-vv` will print the result of the encoding/decoding operations and `-vvv` will print all of the hamming algorithm steps.
- **-h**: prints the help text.

#### Examples

- **Encode the file cat.jpg into the secure file cat.jpg.wham** 

`hamming_check -e cat.jpg cat.jpg.wham`

- **Decode the secure file cat.jpg.wham into the file cat.jpg.wham**

`hamming_check -d cat.jpg.wham cat.jpg`

- **Encode the file cat.jpg into the secure file cat.jpg.wham using a 4096 bytes hamming code**

`hamming_check -e -b 4096 cat.jpg cat.jpg.wham`

- **decode the secure file cat.jpg.wham into the file cat.jpg using a 4096 bytes hamming code**

`hamming_check -d -b 4096 cat.jpg.wham cat.jpg`

- **Encode the string "test" into the secure file file.txt.wham**

`echo -n "test" | hamming_check -e file.txt.wham`

- **Encode the string "test" and print the encoded result to STDOUT**

`echo -n "test" | hamming_check -e`

- **Decode the encoded string <STR> and print the decoded result to STOUT**

`echo -n <STR> | hamming_check -d`

- **Decode the encoded string <STR> and save the result to file.txt**

`echo -n <STR> | hamming_check -d file.txt`

- **Decode the file.txt.wham and print the results to STDOUT**

`hamming_check -d file.txt.wham`

## `hamming_check` library

### Description

`hamming_check` is a library for encoding and decoding binary data using the hamming code.

### Usage

#### `Hamming` Module

Encode and decodes datas using the hamming code of a given `buffer_size` in bytes.

```python
from hamming_check import Hamming, DecodeStatus, DecodeResult, VerbosityTypes
...
hamming = Hamming(buffer_size=1, verbose=VerbosityTypes.QUIET)
size_of_encoded_data = hamming.get_number_of_output_bytes()
encoded_data = hamming.encode(b't')
...
decoded_result = hamming.decode(encode)
decoded_data, decoded_status = decoded_result.get_data(), decoded_result.get_status()
```

#### `io` Module

Abstractions over files and bytes. The `Bytes` class is inherited from the [bitarray](https://pypi.org/project/bitarray/) and the `Files` class is just a wrapper for the python file interface.

```python
from hamming_check import Hamming, DecodeStatus, DecodeResult, VerbosityTypes, File, Bytes
...

hamming = Hamming(buffer_size=2, verbose=VerbosityTypes.QUIET)
input_file = File(open("input_file.txt", "rb"), bytes_per_read=2)
output_file = File(open("output_file.txt", "wb"))

# read data, encodes it, flips a bit and then write
for data in input_file:
  encoded_data = hamming.encode(data)
  bytes = Bytes(encoded_data)
  bytes[0] ^= 1
  output_file.write(bytes.tobytes())

input_file.close()
output_file.close()
```

### Example

Send a encoded file over the network and check it for corruption.

#### Client Code

- [client.py](./examples/send_over_network/client.py): Read a [image](./examples/send_over_network/really_cool_cat.jpg) 4096 bytes per time, encode that chunk of bytes, add a random noise to the encoded data and sends it over the network.

```python
#!/usr/bin/env python
from random import randint, random
import socket
from argparse import ArgumentParser
from math import e

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
```

#### Server Code

- [server.py](./examples/send_over_network/client.py): Receives encoded data throught the network, decodes it, tries to recover noisy data and then sava it to a output file

```python
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
```

#### Putting all together

#### Run server code

```bash
./examples/send_over_network/server.py -f out.jpg
```

#### Run client code

```bash
./examples/send_over_network/examples.py -f ./examples/send_over_network/really_cool_cat.jpg
```

#### Check out.jpg

Even though was added noise to the data, the server was able to recover the image.
