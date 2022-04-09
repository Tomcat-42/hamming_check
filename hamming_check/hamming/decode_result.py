from __future__ import annotations

from .decode_status import DecodeStatus


class DecodeResult(object):
    """Result of a decode operation"""

    def __init__(self,
                 data: bytes = 0,
                 status: DecodeStatus = DecodeStatus.NO_ERROR):
        self.__data = data
        self.__status = status

    def set_data(self, data) -> DecodeResult:
        setattr(self, "__data", data)
        return self

    def get_data(self) -> bytes:
        return getattr(self, "__data")

    def set_status(self, status: DecodeStatus) -> DecodeResult:
        setattr(self, "__status", status)
        return self

    def get_status(self) -> DecodeStatus:
        return getattr(self, "__status")
