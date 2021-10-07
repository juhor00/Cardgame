class Client:
    """
    Connected client
    """
    def __init__(self, socket, uid):
        """
        :param socket: socket
        :param uid: uid
        """

        self.socket = socket
        self.uid = uid
        self.name = f"Player {uid}"
        self.ready = False
        self.in_game = False

    def __str__(self):
        return self.get_name()

    def play(self):
        self.in_game = True

    def stop_playing(self):
        self.in_game = False

    def is_playing(self):
        return self.in_game

    def get_socket(self):
        return self.socket

    def get_uid(self):
        return self.uid

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