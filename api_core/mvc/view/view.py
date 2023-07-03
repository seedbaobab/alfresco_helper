from termcolor import colored, cprint

import colorama as colorama

from api_core.exception.api_exception import ApiException
from api_core.helper.string_helper import StringHelper
from api_core.mvc.view.message_type import MessageType


class View:
    """
    Base class for views.
    """

    def __init__(self, width: int):
        """
        Initialize a new instance of 'View' class.
        :param width: The maximum width of the screen.
        """
        colorama.init()
        self.__width: int = width
        self.__space: int = MessageType.maximum_space()
        self.__maximum_row_width: int = self.__width - 4

    def main_title(self, api_name: str):
        """
        Print the main title of the application to standard output.
        :param api_name: API name.
        """
        self.separation()
        self.__start("> Running {0}".format(api_name))
        self.separation()

    def end_title(self, api_name: str):
        """
        Print the end title of the application to standard output.
        :param api_name: API name.
        """
        self.__end("> End of execution of {0}".format(api_name))
        self.separation()

    def get_input(self, message: str) -> str:
        """
        Print a message and allow the user to type a response.
        :param message: The message to print on the output.
        :return: The user's response.
        """
        self.__print_typed_message(MessageType.INPUT, message)
        client_input: str = input()
        return client_input

    def get_bool_input(self, message: str) -> bool:
        """
        Print a message and allow the user to type a response.
        :param message: The message to print on the output.
        :return: The user's response.
        """
        self.__print_typed_message(MessageType.INPUT, message)
        client_input: str = input()
        if StringHelper.is_empty(client_input) or client_input.__eq__("n"):
            return False
        elif client_input.__eq__("y"):
            return True
        raise ApiException("Your answer is invalid. It can be empty (False), equal to 'n' (False) or 'y' (True).")

    def exception(self, exception: ApiException):
        """
        Print an exception on the standard output.
        :param exception: The exception to print.
        """
        # Print the error message exception.
        self.error(str(exception))
        # Print the manual command if necessary.
        if exception.has_manual:
            if isinstance(exception.manuals, list):
                for manual in exception.manuals:
                    self.manual(manual.to_str())
            else:
                self.manual(exception.manuals.to_str())

    def separation(self):
        """
        Print a separation line on the output.
        """
        print(self.__fill_line("-"))

    def empty(self):
        """
        Print a white line on the standard output.
        """
        print(self.__fill_line(" "))

    def info(self, message: str):
        self.__print_typed_message(MessageType.INFO, message)

    def error(self, message: str):
        """
        Print an error message to the output.
        :param message: The error message.
        """
        self.__print_typed_message(MessageType.ERROR, message)

    def manual(self, message: str = ""):
        """
        Print a manual on the output.
        :param message: The manual output.
        """
        self.__print_typed_message(MessageType.MANUAL, message)
        self.separation()

    def success(self, message: str = ""):
        """
        Print a success message on the output.
        :param message: The message to print on the output.
        """
        self.__print_typed_message(MessageType.SUCCESS, message)

    def warning(self, message: str = ""):
        """
        Print a warning message on the output.
        :param message: The message to print on the output.
        """
        self.__print_typed_message(MessageType.WARN, message)
        # self.separation()

    def __start(self, message: str):
        """
        Print a start message on the output.
        :param message: The message to print on the output.
        """
        self.__print_typed_message(MessageType.START, message)

    def __end(self, message: str):
        """
        Print on the standard output an end message.
        :param message: The message to print on the standard output.
        """
        self.separation()
        self.__print_typed_message(MessageType.END, message)

    def __print_typed_message(self, message_type: MessageType, message: str):
        """
        Print a typed message on the standard output.
        :param message_type:  The message type.
        :param message: The message to print.
        """
        message_to_print: str = "[{0}] {1}".format(message_type.value.ljust(self.__space), message)

        for line in self.__split_in_lines(message_to_print):
            if message_type.value.__eq__("ERROR"):
                print(colored("| {0} |".format(line.ljust(self.__maximum_row_width)), "light_red"))
            elif message_type.value.__eq__("SUCCESS"):
                print(colored("| {0} |".format(line.ljust(self.__maximum_row_width)), "light_green"))
            elif message_type.value.__eq__("WARNING"):
                print(colored("| {0} |".format(line.ljust(self.__maximum_row_width)), "light_yellow"))
            elif message_type.value.__ne__("INPUT"):
                print("| {0} |".format(line.ljust(self.__maximum_row_width)))
            else:
                cprint("| {0}: ".format(line), "white", end='')

    def __fill_line(self, character: str) -> str:
        """
        Return a filled line with the character in parameter.
        :param character: The character that fills the line.
        :return: A line filled with the character in parameter.
        """
        return "|{0}|".format(character * (self.__width - 2))

    def __split_in_lines(self, message: str):
        """
        Split a message into a line array.
        :param message: The message to split.
        :return: The message split in a line array.
        """
        result: [str] = []
        messages: list[str] = message.splitlines()
        if len(message).__le__(self.__maximum_row_width) and len(messages).__lt__(2):
            result.append(message)
            return result

        max_line: int = self.__maximum_row_width
        maximum: int = self.__space + 3

        messages: list[str] = message.splitlines()
        while len(messages).__gt__(0):
            token: str = messages.pop(0)
            if (len(token) + maximum).__gt__(max_line):
                if len(result).__gt__(0):
                    result.append("{0}{1}".format("".ljust(maximum), token[:max_line]))
                else:
                    result.append(token[:max_line])
                messages.insert(0, token[max_line:])
            else:
                if len(result).__gt__(0):
                    result.append("{0}{1}".format("".ljust(maximum), token))
                else:
                    result.append(token)

        return result
