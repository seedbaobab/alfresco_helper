from enum import Enum


class MessageType(Enum):
    """
    Enumeration for available message types.
    """
    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    WARN: str = "WARNING"
    ERROR: str = "ERROR"
    INPUT: str = "INPUT"
    SUCCESS: str = "SUCCESS"
    MANUAL: str = "MANUAL"
    START: str = "START"
    END: str = "END"

    @staticmethod
    def maximum_space() -> int:
        """
        Get the maximum size (in number of characters) of the largest enumeration.
        :return: The maximum size (in number of characters) of the largest enumeration.
        """
        value: int = 0
        for enum_value in MessageType:
            len_enum_value: int = len(enum_value.value)
            if len_enum_value.__gt__(value):
                value = len_enum_value
        return value
