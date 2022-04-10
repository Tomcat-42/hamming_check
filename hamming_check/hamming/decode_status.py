from enum import IntFlag


class DecodeStatus(IntFlag):
    """
    Possible decode status values.
    """

    NO_ERROR = 0
    SINGLE_ERROR_CORRECTED = 1
    DOUBLE_ERROR_DETECTED = 2

    @classmethod
    def _missing_(cls, value):
        return DecodeStatus.NO_ERROR
