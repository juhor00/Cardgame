"""
Common utilities
"""


import threading


def split_json(json_obj):
    """
    Splits a json object if it sends multiple packets once
    :param json_obj: str
    :return: list of str
    """
    json_objects = []
    active_object = ""
    open_brackets = 0
    for char in json_obj:
        # Start
        if char == '{':
            active_object += char
            open_brackets += 1
        # End
        elif char == '}':
            active_object += char
            open_brackets -= 1
            if open_brackets == 0:
                json_objects.append(active_object)
                active_object = ""
        # Continue
        elif active_object != "":
            active_object += char
    return json_objects


def new_thread(target, daemon=True, args=()):
    thread = threading.Thread(target=target, args=args, daemon=daemon)
    thread.start()


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args):
        e = lambda: None
        e.data = eval(args[0])
        e.widget = widget
        return e,

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format('+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)


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