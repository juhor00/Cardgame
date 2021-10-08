

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

            old_uids = set(self.client.status.get_all_opponent_uids())
            old_uids.add(self.client.status.get_uid())

            new_uids = set()
            players = data["players"]
            for player in players:
                uid = player["uid"]
                new_uids.add(uid)
                name = player["name"]
                ready = player["ready"]
                if uid is not self.client.status.get_uid():

                    self.client.status.add_opponent(uid, name)
                    self.client.status.set_opponent_status(uid, ready)

            remove_uids = old_uids - new_uids
            for uid in remove_uids:
                self.client.status.remove_opponent(uid)

        if "start" in data:
            if data["start"]:
                self.client.status.set_lobby_status(False)

    def turnlist_event(self, data: dict):
        """
        Handle turnlist events
        :param data: dict
        """
        for player in data:
            uid = player["uid"]
            turn = player["turn"]
            if uid == self.client.status.get_uid():
                self.client.status.set_turn(turn)
            else:
                self.client.status.set_opponent_turn(uid, turn)

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

        if "turn" in data:
            turn = data["turn"]
            self.client.status.set_turn(turn)

    def opponent_event(self, data: dict):
        """
        Handle opponent events
        :param data: dict
        """
        for opponent in data:
            print(opponent)
            uid = opponent["uid"]
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
        print("Claimgrid event")
        if "allowed" in data:
            allowed = data["allowed"]
            self.client.status.set_allowed_claims(allowed)
        if "denied" in data:
            denied = data["denied"]
            self.client.status.set_denied_claims(denied)
