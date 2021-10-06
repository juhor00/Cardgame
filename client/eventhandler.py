

class EventHandler:

    def __init__(self, client):
        """
        Handle GUI events
        :param client: Client
        """
        self.client = client
        print("UID:", self.client.status.get_uid())

        self.event_types = {
            "lobby": lambda msg: self.lobby_event(msg),
            "turnlist": lambda msg: self.turnlist_event(msg),
            "deck": lambda msg: self.deck_event(msg),
            "game": lambda msg: self.game_event(msg),
            "opponents": lambda msg: self.opponent_event(msg),
            "player": lambda msg: self.player_event(msg),
            "claimgrid": lambda msg: self.claimgrid_event(msg)
        }

    def new(self, message: dict):
        """
        Handle top level events
        :param message: dict
        """
        for key in message:
            self.event_types[key](message[key])

        self.client.update_gui()

    def lobby_event(self, data: dict):
        """
        Handle lobby events
        :param data: dict
        """

        # Lobby events are always in lobby
        self.client.status.set_lobby_status(True)

        if "players" in data:
            players = data["players"]
            for player in players:
                uid = player["uid"]
                name = player["name"]
                ready = player["ready"]
                if uid is not self.client.status.get_uid():

                    self.client.status.add_opponent(uid, name)
                    self.client.status.set_opponent_status(uid, ready)

        if "start" in data:
            self.client.status.set_lobby_status(False)

    def turnlist_event(self, data: dict):
        """
        Handle turnlist events
        :param data: dict
        """

    def deck_event(self, data: dict):
        """
        Handle deck events
        :param data: dict
        """
        if "amount" in data:
            amount = data["amount"]
            self.client.status.set_deck_amount(amount)

    def game_event(self, data: dict):
        """
        Handle game events
        :param data: dict
        """
        if "amount" in data:
            amount = data["amount"]
            self.client.status.set_gamedeck_amount(amount)
        if "latest" in data:
            claim_data = data["latest"]
            amount = claim_data["amount"]
            rank = claim_data["rank"]
            self.client.status.set_claim(amount, rank)

        if "display" in data:
            cards = data["display"]
            self.client.status.set_display(cards)

    def opponent_event(self, data: dict):
        """
        Handle opponent events
        :param data: dict
        """
        for opponent in data:
            uid = opponent["id"]
            amount = opponent["amount"]
            self.client.status.set_opponent_amount(uid, amount)

    def player_event(self, data: dict):
        """
        Handle player events
        :param data: dict
        """
        if "cards" in data:
            cards = data["cards"]
            self.client.status.set_hand_cards(cards)

    def claimgrid_event(self, data: dict):
        """
        Handle claimgrid events
        :param data: dict
        """
        if "allowed" in data:
            allowed = data["allowed"]
            self.client.status.set_allowed_claims(allowed)
        if "denied" in data:
            denied = data["denied"]
            self.client.status.set_denied_claims(denied)