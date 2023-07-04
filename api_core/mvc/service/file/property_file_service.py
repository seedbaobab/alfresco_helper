class PropertyFileService:

    def __init__(self):
        pass

    @staticmethod
    def reset(filepath: str):
        open(filepath, "w").close()

    def add_comment(self, filepath: str, line: str):
        self.__append(filepath, "# {0}".format(line))

    def add_property(self, filepath: str, property_id: str, property_value: str):
        self.__append(filepath, "{0}={1}".format(property_id, property_value))

    @staticmethod
    def __append(filepath: str, line: str):
        with open(filepath, "a") as writer:
            writer.write("{0}\n".format(line))
