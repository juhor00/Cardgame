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
            self.gui.show_error("Server offline")
            self.connected = False

    def player_event(self, data):
        """
        Handles player events
        :param data: JSON data
        """
        if "add" in data:
            self.gui.add_cards(data["add"])

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

    def event(self, message):
        """
        Passes data to their handlers
        :param message: received socket message
        """
        data = json.loads(message)

        if "player" in data:
            new_thread(lambda: self.player_event(data["player"]))

        if "opponent" in data:
            new_thread(lambda: self.opponent_event(data["opponent"]))

        if "deck" in data:
            new_thread(lambda: self.deck_event(data["deck"]))

        if "game" in data:
            new_thread(lambda: self.game_event(data["game"]))

        if "sidebar" in data:
            new_thread(lambda: self.sidebar_event(data["sidebar"]))

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
        json_obj = json.dumps(data)
        self.send(json_obj)

    def send(self, json_obj):
        """
        Send json object to server
        :param json_obj: JSON data
        """
        byte_obj = bytes(json_obj, encoding="UTF-8")
        if self.connected:
            self.server.send(byte_obj)
