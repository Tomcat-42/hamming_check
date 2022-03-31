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
def bin_file() -> str:
    """Return the path for a bin file for use with tests.

    :return: A string.
    :rtype: str
    """

    files = load_test_data()
    return files['bin']
