import json
import socket
from gui import *
from utilities import *


class Client:

    def __init__(self, gui: Gui):
        """
        Link GUI to client
        :param gui: Gui instance
        """
        self.gui = gui

        yaml = Parser("settings/network.yml")
        self.settings = yaml.read()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = self.settings["host"]                  # Static ip
        # host = socket.gethostname()  # Localhost
        port = int(self.settings["port"])
        print("Connecting...")
        try:
            self.server.connect((host, port))
            print("Connected")
            self.connected = True
        except socket.error:
            self.gui.show_message("Server offline")
            self.connected = False

    def player_event(self, data):
        """
        Handles player events
        :param data: JSON data
        """
        if "add" in data:
            self.gui.hand.add_cards(data["add"])

    def opponent_event(self, data):
        """
        Handles opponent events
        :param data: JSON data
        """
        for opponent in data:
            self.gui.update_opponent(opponent)

    def deck_event(self, data):
        """
        Handles deck events
        :param data: JSON data
        """
        if "amount" in data:
            self.gui.deck.set_amount(data["amount"])
        if "drawtop" in data:
            print(data["drawtop"])

    def game_event(self, data):
        """
        Handles game events
        :param data: JSON data
        """
        if "amount" in data:
            self.gui.gamepile.set_amount(data["amount"])

    def sidebar_event(self, data):
        """
        Handles sidebar events
        :param data: JSON data
        """

    def lobby_event(self, data):
        """
        Handles lobby events
        :param data: JSON data
        """
        if "opponents" in data:
            self.gui.lobby.remove_all()
            for opponent in data["opponents"]:
                name = opponent["name"]
                ready = bool(opponent["ready"])
                self.gui.lobby.add_opponent(name, ready)

        if "start" in data:
            if bool(data["start"]):
                self.gui.draw_window()

    def event(self, message):
        """
        Passes data to their handlers
        :param message: received socket message
        """
        data = json.loads(message)

        if "player" in data:
            new_thread(lambda: self.player_event(data["player"]))

        if "opponents" in data:
            new_thread(lambda: self.opponent_event(data["opponents"]))

        if "deck" in data:
            new_thread(lambda: self.deck_event(data["deck"]))

        if "game" in data:
            new_thread(lambda: self.game_event(data["game"]))

        if "sidebar" in data:
            new_thread(lambda: self.sidebar_event(data["sidebar"]))

        if "lobby" in data:
            new_thread(lambda: self.lobby_event(data["lobby"]))

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode("UTF-8")
                for json_obj in split_json(message):
                    event_thread = threading.Thread(
                        target=lambda: self.event(json_obj))
                    event_thread.start()
            except socket.error:
                print("An error occurred!")
                self.server.close()
                break

    def send_general(self, message):
        """
        Send general data
        :param message: str
        """
        data = {"general": message}
        self.send(data)

    def send_lobby(self, ready, name=None):
        """
        Send lobby messages
        :param ready: bool (int)
        :param name: str
        """
        lobby_data = {"ready": ready}
        if name is not None:
            lobby_data["name"] = name
        data = {"lobby": lobby_data}
        self.send(data)

    def send_deck(self, state):
        """
        Send deck messages
        :param state: bool (int)
        """
        data = {"game": {"deck": state}}
        self.send(data)

    def send_suspect(self, state):
        """
        Send suspect messages
        :param state: bool (int)
        """
        data = {"game": {"suspect": state}}
        self.send(data)

    def send_played_cards(self, cards, claim):
        """
        Send player cards message with claim
        :param cards: list of str
        :param claim: str
        """
        data = {"game": {"played": cards,
                         "claimed": claim}}
        self.send(data)

    def send(self, data):
        """
        Send json object to server
        :param data: dict
        """
        json_obj = json.dumps(data)
        byte_obj = bytes(json_obj, encoding="UTF-8")
        if self.connected:
            self.server.send(byte_obj)
