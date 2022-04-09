"""

tests.conftest.py
~~~~~~~~~~~~~~~~~

This module is used by PyTest to detect test fixtures that are used by
multiple test modules. For more imformation on fixtures in PyTest, see
https://docs.pytest.org/en/latest/fixture.html.
"""

import json
from typing import Any, Dict

import pytest

def load_test_data() -> Dict[str, Any]:
    """Load test data from JSON file.

    :return: Test data.
    :rtype: Dict[str, Any]
    """

    config_file_path = 'tests/test_data/test_files.json'
    with open(config_file_path) as file:
        json_data = file.read()

    data = json.loads(json_data)
    return data['files']


@pytest.fixture
def text_file() -> str:
    """Return the path for a text file for use with tests.

    :return: A string.
    :rtype: str
    """

    files = load_test_data()
    return files['text']

@pytest.fixture
def text_file_single_byte() -> list[bytes]:
    """Return the bytes that match the text file content

    :return: A bytestring.
    :rtype: list[bytes]
    """

    return [b't', b'e', b's', b't', b'e',b'\n']

@pytest.fixture
def text_file_four_bytes() -> list[bytes]:
    """Return the bytes that match the text file content

    :return: A bytestring.
    :rtype: list[bytes]
    """

    return [b'test', b'e\n']

@pytest.fixture
def bytes_single_byte() -> bytes:
    """Return a single byte

    :return: A bytestring.
    :rtype: bytes
    """

    # 0b01100001
    return b'a'

@pytest.fixture
def bytes_single_byte_bits() -> list[int]:
    """Return a single byte in bits

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    # 0b01100001
    return [
        0, 1, 1, 0, 0, 0, 0, 1,
    ]

@pytest.fixture
def bytes_three_bytes() -> bytes:
    """Return a single byte

    :return: A bytestring.
    :rtype: str
    """

    # 0b01100001
    # 0b01100010
    # 0b01100011
    return b'abc'

@pytest.fixture
def bytes_three_bytes_bits() -> list[int]:
    """Return three byte in bits

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    # 0b01100001
    # 0b01100010
    # 0b01100011
    return [ 
        0, 1, 1, 0, 0, 0, 0, 1,
        0, 1, 1, 0, 0, 0, 1, 0,
        0, 1, 1, 0, 0, 0, 1, 1
    ] 

@pytest.fixture
def bytes_three_bytes_bits_little_endian() -> list[int]:
    """Return three byte in bits

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    # 0b01100001
    # 0b01100010
    # 0b01100011
    return [
        1, 0, 0, 0, 0, 1, 1, 0,
        0, 1, 0, 0, 0, 1, 1, 0,
        1, 1, 0, 0, 0, 1, 1, 0
    ]

@pytest.fixture
def t_bytes() -> bytes:

    return b't'

@pytest.fixture
def t_bits() -> list[int]:
    """Return a list of integers, 0 or 1.

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    return [
        0, 0, 1, 0, 1, 1, 1, 0
    ]


@pytest.fixture
def t_hammified() -> list[int]:
    """Return a list of integers, 0 or 1.

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    return [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0
    ]

@pytest.fixture
def t_hammified_bit4_flipped() -> list[int]:
    """Return a list of integers, 0 or 1.

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    return [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0
    ]

@pytest.fixture
def t_hammified_bit4_bit11_flipped() -> list[int]:
    """Return a list of integers, 0 or 1.

    :return: A list of integers, 0 or 1.
    :rtype: list[int]
    """

    return [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0
    ]


@pytest.fixture
def bin_file() -> str:
    """Return the path for a bin file for use with tests.

    :return: A string.
    :rtype: str
    """

    files = load_test_data()
    return files['bin']
