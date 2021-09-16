class Client:
    """
    Connected client
    """
    def __init__(self, id):
        """
        :param id: Client's id
        """

        self.id = id
        self.name = f"Player {id}"
        self.ready = False

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