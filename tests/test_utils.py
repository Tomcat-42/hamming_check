"""
tests.test_utils.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the Utils Module
"""

from hamming_check.utils import Utils


class TestUitls:
    """Test suite for Input module."""

    def test_utils_is_power_of_two(self, power_of_two: int):
        """Test Utils class."""

        assert Utils.is_power_of_two(power_of_two)

    def test_utils_not_is_power_of_two(self, non_power_of_two: int):
        """Test Utils class."""

        assert Utils.is_power_of_two(non_power_of_two) is False

    def test_utils_is_not_power_of_two_zero(self, non_power_of_two_zero: int):
        """Test Utils class."""

        assert Utils.is_power_of_two(non_power_of_two_zero) is False

    def test_utils_not_is_not_power_of_two_zero(self,
                                                non_power_of_two_zero: int):
        """Test Utils class."""

        assert not Utils.is_power_of_two(non_power_of_two_zero) is True
