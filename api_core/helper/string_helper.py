from typing import Optional


class StringHelper:
    """
    Helper class for String.
    """

    @staticmethod
    def is_empty(value: Optional[str]) -> bool:
        """
        Method checking if the parameter value is null or empty.
        :param value: The value to test.
        :return: True if the value is None or empty.
        """
        return True if value is None or value.strip().__eq__("") else False

    @staticmethod
    def has_space(value: Optional[str]) -> bool:
        """
        Method that checks if the parameter value contains a space.
        :param value: The value to test.
        :return: True if the parameter value contains space is None or empty.
        """
        return False if value is None or not (' ' in value.strip()) else True

    @staticmethod
    def is_alphabetic(value: str) -> bool:
        return any(c.isalpha() for c in value)

    @staticmethod
    def to_camel_case(value: str) -> str:
        return sub(r"(_|-)+", " ", value).title().replace(" ", "")

    @staticmethod
    def to_snake_case(value: str) -> str:
        filename: str = re.sub('([A-Z]{1})', r'-\1', value).lower()
        return "{0}-model".format(filename)
