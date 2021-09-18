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

    def new(self, message: dict):
        """
        Handle top level events
        :param message: dict
        """
        if "lobby" in message:
            self.lobby_event(message["lobby"])

        if "turnlist" in message:
            self.turnlist_event(message["turnlist"])

        if "deck" in message:
            self.deck_event(message["deck"])

        if "game" in message:
            self.game_event(message["game"])

        if "opponents" in message:
            self.opponent_event(message["opponents"])

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
        players = []
        for player in data:
            name = player["name"]
            user_id = player["id"]
            if user_id == self.id:
                name = "You"
            players.append(name)
        self.gui.gamewindow.turn.add_players(players)

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
        if "amount" in data:
            amount = data["amount"]
            self.gui.gamewindow.gamedeck.set_amount(amount)

    def opponent_event(self, data: dict):
        """
        Handle opponent events
        :param data: dict
        """
        for opponent in data:
            name = opponent["name"]
            amount = opponent["amount"]
            self.gui.gamewindow.opponents.set_amount(name, amount)


