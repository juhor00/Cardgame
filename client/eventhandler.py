

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
        - Other players (by UID):
            - Name
            - Ready
        - Start
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

    def deck_event(self, data: dict):
        """
        Handle deck events
        - Amount
        :param data: dict
        """
        if "amount" in data:
            amount = data["amount"]
            self.client.status.set_deck_amount(amount)

    def game_event(self, data: dict):
        """
        Handle game events
        - Game Deck amount
        - Latest claim
        - Display (suspect cards shown)
        - Duration (how long until deck is discarded)
        - Turn
        :param data: dict
        """
        actions = {
            "amount": lambda amount: self.client.status.set_gamedeck_amount(amount),
            "latest": lambda claim: self.client.status.set_claim(claim["amount"], claim["rank"]),
            "display": lambda cards: self.client.status.set_display(cards),
            "duration": lambda duration: self.client.status.set_duration(duration),
            "turn": lambda turn: self.client.status.set_turn(turn),
        }

        for key in data:
            actions[key](data[key])

    def opponent_event(self, data: dict):
        """
        Handle opponent events (by UID)
        - Amount
        - Turn
        :param data: dict
        """
        actions = {
            "amount": lambda amount: self.client.status.set_opponent_amount(uid, amount),
            "turn": lambda turn: self.client.status.set_opponent_turn(uid, turn),
            "name": lambda name: None,
            "played": lambda played: self.client.status.set_opponent_played(uid, played),
            "suspected": lambda suspected: self.client.status.set_opponent_suspected(uid, suspected),
        }
        for opponent in data:
            uid = opponent["uid"]
            opponent.pop("uid")
            for key in opponent:
                value = opponent[key]
                actions[key](value)

    def player_event(self, data: dict):
        """
        Handle player events
        - Cards
        - Turn
        :param data: dict
        """

        actions = {
            "cards": lambda cards: self.client.status.set_hand_cards(cards),
            "turn": lambda turn: self.client.status.set_turn(turn),
        }

        for key in data:
            value = data[key]
            actions[key](value)

    def claimgrid_event(self, data: dict):
        """
        Handle claimgrid events
        - Allowed
        - Denied
        :param data: dict
        """
        self.client.status.set_allowed_claims(data["allowed"])
        self.client.status.set_denied_claims(data["denied"])
