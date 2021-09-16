import deck
from player import Player
from utilities import *


class CardGame:

    def __init__(self, server):
        """
        Initialize game
        :param server: Server
        """

        self.server = server

        self.players = {}
        self.deck = deck.Deck()
        self.gamedeck = deck.Deck()
        self.turn = 0
        self.last_claimed_rank = None
        self.in_lobby = True
        self.latest_claim = None

    def broadcast_lobby(self):
        """
        Broadcast lobby info
        """
        for send_client in self.players:
            opponents = []
            for other_client in self.players:
                if not other_client == send_client:
                    player = self.players[other_client]
                    name = player.get_name()
                    ready = int(player.is_ready())
                    opponents.append({"name": name, "ready": ready})
            opponents_info = {"opponents": opponents}
            lobby_info = {"lobby": opponents_info}
            self.server.send_dict(lobby_info, send_client)

    def lobby_event(self, client, address, info):
        """
        Handles lobby events
        :param client: socket
        :param address: IP and port
        :param info: dict
        """
        if client not in self.players:
            player = Player(client, address)
            self.players[client] = player
        else:
            player = self.players[client]
        if "name" in info:
            name = info["name"]
            player.add_name(name)

        ready = bool(info["ready"])
        player.set_ready(ready)
        self.broadcast_lobby()
        self.check_start()

    def add_player(self, client, address):
        """
        Adds a new player
        :param client: socket
        :param address: IP and port
        """
        player = Player(client, address)
        self.players[client] = player
        if self.in_lobby:
            self.broadcast_lobby()

    def remove_player(self, client):
        """
        Remove disconnected player
        :param client: socket
        """
        del self.players[client]
        if self.in_lobby:
            self.broadcast_lobby()
        else:
            self.update()

    def check_start(self):
        """
        Check if all players are ready and start the game
        """
        if len(self.players) == 0:
            return
        for ip in self.players:
            if not self.players[ip].is_ready():
                return
        self.start()

    def start(self):
        """
        Start the game, send info
        """
        self.deck.empty()
        self.gamedeck.empty()

        self.deck.generate_cards()
        self.deck.shuffle()
        for client in self.players:
            self.draw_cards(self.deck, client, 5)
        self.update()
        info = {"lobby": {"start": 1}}
        self.server.broadcast(info)

    def update(self):
        """
        Send shared, updated info to all clients during game
        """
        self.update_opponents()
        # Deck
        deck_info = {"amount": self.deck.get_amount()}

        # Game
        game_info = {"amount": self.gamedeck.get_amount()}

        # Complete info
        info = {"deck": deck_info,
                "game": game_info}
        self.server.broadcast(info)

    def update_opponents(self):
        """
        Update opponent situation for each player
        """
        for client in self.players:
            player = self.players[client]
            opponents_info = []
            for other_client in self.players:
                other_player = self.players[other_client]
                if other_player != player:
                    opponents_info.append({
                        "amount": other_player.get_amount(),
                        "name": other_player.get_name()
                    })
            info = {"opponents": opponents_info}
            self.server.send_dict(info, client)

    def draw_cards(self, source: deck.Deck, client, amount):
        """
        Draw cards from source to dest (from top)
        :param source: Deck
        :param client: socket
        :param amount: int
        """
        player = self.players[client]
        added_cards = []
        for _ in range(amount):
            if not source.is_empty():
                card = source.get_top()
                player.add(card)
                added_cards.append(str(card))
            else:
                break
        self.server.send_dict({"player": {"add": added_cards}}, client)

    def is_allowed_rank(self, rank):
        """
        Return True if rank is allowed
        :param rank: int
        :return: bool
        """
        if rank == 2:
            return True
        if rank < self.last_claimed_rank:
            return False
        if self.last_claimed_rank == 2:
            return False
        if rank == 10:
            if self.last_claimed_rank > 9:
                return False
        if rank == 14:
            if self.last_claimed_rank < 11:
                return False
        if self.last_claimed_rank < 7:
            return False
        if rank == 10 or rank == 14:
            if self.deck.is_empty():
                return False
        if rank > 10:
            if not self.deck.is_empty():
                return False

        return True



