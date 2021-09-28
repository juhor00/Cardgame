class Client:
    """
    Connected client
    """
    def __init__(self, socket, id):
        """
        :param socket: socket
        :param id: id
        """

        self.socket = socket
        self.id = id
        self.name = f"Player {id}"
        self.ready = False

    def __str__(self):
        return self.get_name()

    def get_socket(self):
        return self.socket

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_name(self, name):
        """
        Sets the name
        :param name: str
        """
        if name:
            self.name = name

    def set_ready(self, state):
        """
        Set readiness state
        :param state: bool
        """
        self.ready = state

    def is_ready(self):
        """
        Return True if ready
        :return: bool
        """
        return self.ready