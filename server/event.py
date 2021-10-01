from game.game import Game
from client import Client


class Event:

    def __init__(self, server):

        self.server = server
        self.in_lobby = True
        self.game = None

        self.clients = []

    def add(self, socket, client_id):
        """
        Add a client and broadcast it to others
        :param socket: socket
        :param client_id: int
        """
        client = Client(socket, client_id)
        self.clients.append(client)

    def remove(self, socket):
        """
        Remove a client
        :param socket: socket
        """
        to_remove = self.get_client_by_socket(socket)
        if to_remove in self.clients:
            self.clients.remove(to_remove)

        for client in self.clients:
            if client.is_playing():
                continue
            self.in_lobby = True
            break
        if len(self.clients) == 0:
            self.in_lobby = True
        print("In lobby: ", self.in_lobby)

        return to_remove

    def get_client_by_socket(self, socket):
        """
        Return client that has given socket
        :param socket: socket
        :return: Client
        """
        for client in self.clients:
            if client.get_socket() == socket:
                return client

    def send(self, client, data):
        """
        Send data to client
        :param client: Client
        :param data: dict
        """
        self.server.send(client.get_socket(), data)

    def sendall(self, data):
        """
        Send data to all clients
        :param data: dict
        """
        for client in self.clients:
            self.send(client, data)

    def new(self, socket, data):
        """
        Handle all events
        :param socket: socket
        :param data: dict
        """
        client = self.get_client_by_socket(socket)
        print(f"{client} sent {data}")
        if "general" in data:
            self.general_event(client, data["general"])
        if "lobby" in data:
            self.lobby_event(client, data["lobby"])
        if "game" in data:
            self.game_event(client, data["game"])

    def general_event(self, client, data):
        """
        Handle general events, network control
        :param client: Client
        :param data: dict
        """
        if data == "connect":
            self.broadcast_lobby()

    def lobby_event(self, client, data):
        """
        Handle lobby events
        :param client: Client
        :param data: dict
        """
        if "name" in data:
            client.set_name(data["name"])
        client.set_ready(data["ready"])
        self.broadcast_lobby()

        if self.check_start():
            self.start()

    def game_event(self, client, data):
        """
        Handle game events
        :param client: Client
        :param data: dict
        """
        if "played" in data:
            cards = data["played"]
            claimed = data["claimed"]
            player = self.get_player(client)
            self.game.play(player, cards, claimed)

        if "suspect" in data:
            player = self.get_player(client)
            self.game.suspect(player)

        self.broadcast_game()

    def broadcast_lobby(self):
        """
        Send lobby data to all players
        """
        if not self.in_lobby:
            return
        players = []
        for client in self.clients:
            players.append({"id": client.get_id(), "name": client.get_name(), "ready": client.is_ready()})
        data = {"lobby": {"players": players, "start": self.check_start()}}
        self.sendall(data)

    def broadcast_game(self):
        """
        Send game data to all players
        - Opponents
        - Deck
        - Gamedeck
        - Players' cards
        """
        if self.in_lobby:
            return
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
        for client in self.clients:
            player_id = client.id
            opponents = []

            for opponent_client in self.clients:
                if opponent_client.id != player_id:
                    player = self.game.turnmanager.get_player(opponent_client.name)
                    amount = player.hand.get_amount()
                    opponents.append({"amount": amount, "name": player.get_name()})

            opponent_data = {"opponents": opponents}
            self.send(client, opponent_data)

    def broadcast_player_data(self):
        """
        Broadcast personal data to each player
        """
        for client in self.clients:
            name = client.name
            player = self.game.turnmanager.get_player(name)
            cards = player.hand.get_cards()
            personal_data = {"player": {"cards": cards}}

            # Turn
            in_turn_id = self.game.turnmanager.get_active_player().get_id()
            if client.id == in_turn_id:
                turn = True
            else:
                if self.game.turnmanager.is_first_round():
                    turn = True
                else:
                    turn = False
            personal_data["game"] = {"turn": turn}

            self.send(client, personal_data)

    def check_start(self):
        """
        Return True if all player are ready in lobby
        :return: bool
        """
        if not self.in_lobby:
            return False

        if len(self.clients) < 2:
            return False
        for client in self.clients:
            if not client.is_ready():
                return False
        return True

    def start(self):
        """

        :return:
        """
        print("START")
        self.in_lobby = False
        players = []
        for client in self.clients:
            client.play()
            players.append((client.get_id(), client.get_name()))
        self.game = Game(players)
        self.game.start()
        self.broadcast_game()

    def get_player(self, client):
        """
        Get game player by client
        :param client: Client
        :return: Player
        """
        return self.game.turnmanager.get_player(client.get_name())
