import socket
import json
import threading

try:
    from .game.game import Game
    from .client import Client
except ImportError:
    from game.game import Game
    from client import Client


def new_thread(target, daemon=True, args=()):
    thread = threading.Thread(target=target, args=args, daemon=daemon)
    thread.start()


class Server:

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "192.168.2.132"
        port = 12345
        self.server.bind((host, port))
        self.server.listen()
        self.id_count = 0
        self.in_lobby = True
        print("Server is online")
        new_thread(self.receive, daemon=False)

        self.game = Game()
        self.clients = {}

    def receive(self):
        """
        New client connections
        """
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} connected!")
            self.id_count += 1
            new_thread(lambda: self.handle(client))
            client.send(bytes(str(self.id_count), encoding="UTF-8"))
            self.clients[client] = Client(self.id_count)

            if self.in_lobby:
                self.broadcast_lobby()

    def handle(self, client):
        """
        Handle connected client
        """
        while True:
            try:
                message = json.loads(client.recv(2048).decode())
                new_thread(lambda: self.event(client, message))
            except socket.error:
                # Disconnect
                client.close()
                print(f"{client} disconnected!")
                self.id_count -= 1
                del self.clients[client]
                if len(self.clients) == 0:
                    self.in_lobby = True
                return

    def send(self, client, data):
        """
        Send data to client
        :param client: socket client
        :param data: data to JSON
        """
        client.send(json.dumps(data).encode("UTF-8"))

    def sendall(self, data):
        """
        Send data to all clients
        :param data: data to JSON
        """
        for client in self.clients:
            self.send(client, data)

    def check_start(self):
        """
        Start the game if all players are ready
        """
        if len(self.clients) < 2:
            return False
        for i in self.clients:
            client = self.clients[i]
            if not client.ready:
                return False
        return True

    def start(self):
        """
        Start the game
        """
        self.in_lobby = False
        data = {"lobby": {"start": True}}
        self.sendall(data)

        players = []
        names = []
        for i in self.clients:
            client = self.clients[i]
            name = client.name
            user_id = client.id
            players.append({"name": name, "id": user_id})
            names.append(name)
        self.sendall({"turnlist": players})

        self.game.start(names)
        self.broadcast_game()
        self.game.print()

    def event(self, client, data):
        """
        Handle an event made by a client
        :param client: socket client
        :param data: bytes
        """
        print(f"{client} sent {data}")
        if "lobby" in data:
            self.lobby_event(client, data["lobby"])

    def lobby_event(self, client, data):
        """
        Handle lobby events
        :param client: socket client
        :param data: dict
        """
        client = self.clients[client]
        if "name" in data:
            client.set_name(data["name"])
        client.set_ready(data["ready"])
        self.broadcast_lobby()

        if self.check_start():
            self.start()

    def broadcast_lobby(self):
        """
        Send lobby data to all players
        """
        players = []
        for i in self.clients:
            client = self.clients[i]
            client_id = client.id
            name = client.name
            ready = client.ready
            players.append({"id": client_id, "name": name, "ready": ready})
        ready = self.check_start()
        data = {"lobby": {"players": players}, "ready": ready}
        self.sendall(data)

    def broadcast_game(self):
        """
        Send game data to all players
        - Opponents
        - Deck
        - Gamedeck
        - Players' cards
        """
        self.broadcast_opponent_data()

        deck_amount = self.game.deck.get_amount()
        deck_data = {"deck": {"amount": deck_amount}}
        self.sendall(deck_data)

        gamedeck_amount = self.game.gamedeck.get_amount()
        gamedeck_data = {"game": {"amount": gamedeck_amount}}
        self.sendall(gamedeck_data)

        self.broadcast_player_data()

    def broadcast_opponent_data(self):
        """
        Send opponent data to each player
        """
        for i in self.clients:
            client = self.clients[i]
            player_id = client.id
            opponents = []

            for j in self.clients:
                opponent_client = self.clients[j]
                if opponent_client.id != player_id:
                    player = self.game.turnmanager.get_player(opponent_client.name)
                    amount = player.get_amount()
                    opponents.append({"amount": amount, "name": player.get_name()})

            opponent_data = {"opponents": opponents}
            self.send(i, opponent_data)

    def broadcast_player_data(self):
        """
        Broadcast player data to each player
        """
        for i in self.clients:
            client = self.clients[i]
            name = client.name
            player = self.game.turnmanager.get_player(name)
            cards = player.hand.get_cards()
            player_data = {"player": {"cards": cards}}
            self.send(i, player_data)



if __name__ == '__main__':
    server = Server()