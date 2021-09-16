import deck


class Player(deck.Deck):

    def __init__(self, client, address):
        super().__init__()
        self.client = client
        self.address = address
        self.name = ""
        self.ready = False

    def add_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def set_ready(self, state):
        self.ready = state

    def is_ready(self):
        return self.ready


