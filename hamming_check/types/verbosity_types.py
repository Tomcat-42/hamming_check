from enum import IntEnum


class VerbosityTypes(IntEnum):
    """
    Possible verbosity values.
    """

    QUIET = 0
    ONLY_ERRORS = 1
    DECODE_ENCODE_RESULTS = 2
    HAMMING_STEPS = 3

    @classmethod
    def _missing_(cls, value):
        return VerbosityTypes.HAMMING_STEPS
