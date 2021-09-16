import socket                   # Import socket module
import json
from utilities import *
import defaultcomms


class Server:

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        network_file = Parser("settings/network.yml")
        network_settings = network_file.read()
        host = network_settings["host"]
        port = int(network_settings["port"])
        self.server.bind((host, port))
        self.server.listen()

        print("Server is online")
        self.clients = {}
        new_thread(self.receive, daemon=False)
        self.game = None

    def __del__(self):
        print("Server shut down")

    def event(self, client, message):
        """
        A server event
        :param client: socket client
        :param message: JSON dict
        """
        data = json.loads(message)
        if "lobby" in data:
            address = self.clients[client]["address"]
            new_thread(lambda: self.game.lobby_event(client, address, data["lobby"]))

    def add_game(self, game):
        """
        Link game object to server
        :param game: Game instnace
        """
        self.game = game

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode("UTF-8")
                new_thread(lambda: self.event(client, message))
            except socket.error:
                client.close()
                print(f"{self.clients[client]['address']} disconnected!")
                self.game.remove_player(client)
                del (self.clients[client])
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} connected!")
            self.clients[client] = {"address": address}
            self.game.add_player(client, address)

            thread = threading.Thread(target=lambda: self.handle(client))
            thread.start()

    def broadcast(self, info):
        """
        Broadcast to all clients
        :param info: dict
        """
        for client in self.clients:
            self.send_dict(info, client)

    @staticmethod
    def send_dict(info, client):
        """
        Sends a dictionary
        :param info: dict
        :param client: socket client
        """
        json_obj = json.dumps(info)
        byte_obj = bytes(json_obj, encoding="UTF-8")
        client.send(byte_obj)
