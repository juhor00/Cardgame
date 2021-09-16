class Parser:
    def __init__(self, filepath):
        try:
            self.file = open(filepath, "r")
        except OSError:
            pass

    def read(self):
        """
        Reads a .yml file and returns dictionary
        :return: dict
        """
        content = {}
        values = []
        key = None

        for line in self.file:
            if line[0] == "#":
                continue
            if line.strip() == "":
                continue

            # New key - value
            if not self.is_list(line):
                # Existing list to dictionary
                if values:
                    content[key] = values
                    values = []
                # New
                pair = line.split(":")
                key = pair[0].strip()
                value = pair[1].strip()
                # Not a new list
                if value != "":
                    content[key] = value
            # Listing
            else:
                value = line.split("-")[-1].strip()
                values.append(value)

        # List ended on file end
        if values:
            content[key] = values

        return content

    @staticmethod
    def print(dictionary):
        """
        Print dictionary
        :param dictionary: dict
        """
        for key in dictionary:
            print(key, dictionary[key])

    @staticmethod
    def is_list(line):
        """
        Return boolean if line is a list format
        :param line: str
        :return: bool
        """
        line = line.strip()
        return line.find("-") == 0


if __name__ == "__main__":
    p = Parser("settings.yml")
    settings = p.read()
    p.print(settings)
