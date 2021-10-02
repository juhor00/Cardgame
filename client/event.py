try:
    from .gui.gui import Gui
except ImportError:
    from gui.gui import Gui


class Event:

    def __init__(self, gui: Gui, user_id: int):
        """
        Handle GUI events
        :param gui: Gui object
        """
        self.gui = gui
        self.id = user_id

        self.event_types = {
            "lobby": lambda msg: self.lobby_event,
            "turnlist": lambda msg: self.turnlist_event,
            "deck": lambda msg: self.deck_event,
            "game": lambda msg: self.game_event,
            "opponents": lambda msg: self.opponent_event,
            "player": lambda msg: self.player_event,
            "claimgrid": lambda msg: self.claimgrid_event
        }

    def new(self, message: dict):
        """
        Handle top level events
        :param message: dict
        """
        for key in message:
            self.event_types[key](message[key])

    def lobby_event(self, data: dict):
        """
        Handle lobby events
        :param data: dict
        """
        if "players" in data:
            players = data["players"]
            self.gui.lobby.remove_all()
            for player in players:
                user_id = player["id"]
                name = player["name"]
                ready = player["ready"]

                if user_id is not self.id:
                    self.gui.lobby.add_opponent(name, ready)

        if "start" in data:
            if data["start"]:
                self.gui.render_gamewindow()
                opponents = self.gui.lobby.get_opponents()
                for opponent in opponents:
                    self.gui.gamewindow.opponents.add(opponent, 0)

    def turnlist_event(self, data: dict):
        """
        Handle turnlist events
        :param data: dict
        """
        # Create turnlist
        if self.gui.gamewindow.turn.is_empty():
            players = []
            for player in data:
                name = player["name"]
                user_id = player["id"]
                if user_id == self.id:
                    name = "You"
                players.append(name)
            self.gui.gamewindow.turn.add_players(players)

        # Update turnlist
        for player in data:
            name = player["name"]
            user_id = player["id"]
            turn = player["turn"]
            if user_id == self.id:
                name = "You"
                self.gui.set_turn(turn)
            self.gui.gamewindow.turn.set_turn(name, turn)

    def deck_event(self, data: dict):
        """
        Handle deck events
        :param data: dict
        """
        if "amount" in data:
            amount = data["amount"]
            self.gui.gamewindow.deck.set_amount(amount)

    def game_event(self, data: dict):
        """
        Handle game events
        :param data: dict
        """
        self.gui.gamewindow.play_cards.empty()
        self.gui.gamewindow.remove_play_cards()
        if "amount" in data:
            amount = data["amount"]
            self.gui.gamewindow.gamedeck.set_amount(amount)
        if "latest" in data:
            claim_data = data["latest"]
            amount = claim_data["amount"]
            rank = claim_data["rank"]
            self.gui.gamewindow.claim.new(amount, rank)

        if "display" in data:
            cards = data["display"]
            if len(cards) == 0:
                self.gui.gamewindow.play_cards.empty()
            else:
                self.gui.gamewindow.play_cards.add_cards(cards)

    def opponent_event(self, data: dict):
        """
        Handle opponent events
        :param data: dict
        """
        for opponent in data:
            name = opponent["name"]
            amount = opponent["amount"]
            self.gui.gamewindow.opponents.set_amount(name, amount)

    def player_event(self, data: dict):
        """
        Handle player events
        :param data: dict
        """
        if "cards" in data:
            cards = data["cards"]
            cards_dict = {}
            for card in cards:
                if card not in cards_dict:
                    cards_dict[card] = 1
                else:
                    cards_dict[card] += 1

            hand = self.gui.gamewindow.hand.get_cards()
            hand_dict = {}
            for card in hand:
                if card not in hand_dict:
                    hand_dict[card] = 1
                else:
                    hand_dict[card] += 1

            for card in cards:
                # Card is missing
                if card not in hand_dict:
                    for _ in range(cards_dict[card]):
                        self.gui.gamewindow.hand.add_card(card)
                # Too many cards in hand
                elif hand_dict[card] > cards_dict[card]:
                    for _ in range(hand_dict[card] - cards_dict[card]):
                        self.gui.gamewindow.hand.remove_card(card)
                # Too few cards in hand
                elif hand_dict[card] < cards_dict[card]:
                    for _ in range(cards_dict[card] - hand_dict[card]):
                        self.gui.gamewindow.hand.add_card(card)

    def claimgrid_event(self, data: dict):
        """
        Handle claimgrid events
        :param data: dict
        """
        if "allowed" in data:
            self.gui.gamewindow.claimgrid.enable_buttons(data["allowed"])
        if "denied" in data:
            self.gui.gamewindow.claimgrid.disable_buttons(data["denied"])
