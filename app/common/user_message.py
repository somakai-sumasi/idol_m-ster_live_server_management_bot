from enum import IntEnum


class MessageType(IntEnum):
    INFO = 0xAAAAAA
    SUCCESS = 0x00CF00
    NOTICE = 0x005FAF
    WARNING = 0xFFCF00
    ERROR = 0xAF0000
