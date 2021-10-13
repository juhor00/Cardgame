from game.game import Game
from client import Client

from time import sleep
from threading import Thread


def new_thread(target, daemon=True, args=()):
    thread = Thread(target=target, args=args, daemon=daemon)
    thread.start()


DISCARD_DURATION = 8
DISPLAY_DURATION = 5


class EventHandler:

    def __init__(self, server):

        self.server = server
        self.in_lobby = True
        self.game = None
        self.displaying = False

        self.clients = []

    def add(self, socket, uid):
        """
        Add a client and broadcast it to others
        :param socket: socket
        :param uid: int
        """
        client = Client(socket, uid)
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

            # Game deck discard check
            if self.game.gamedeck.to_discard():
                self.broadcast_game()
                self.broadcast_pause()
                self.broadcast_discard(DISCARD_DURATION)
                new_thread(lambda: self.wait_for_discard(wait=DISCARD_DURATION))
            else:
                self.broadcast_game()

        if "suspect" in data:
            player = self.get_player(client)
            if self.game.can_suspect(player):

                self.broadcast_suspect(player)
                self.game.suspect(player)
                self.displaying = True
                new_thread(lambda: self.wait_for_display(wait=DISPLAY_DURATION))

    def broadcast_lobby(self):
        """
        Send lobby data to all players
        """
        if not self.in_lobby:
            return
        players = []
        for client in self.clients:
            players.append({"uid": client.get_uid(), "name": client.get_name(), "ready": client.is_ready()})
        data = {"lobby": {"players": players, "start": self.check_start()}}
        self.sendall(data)

    def broadcast_game(self):
        """
        Send game data to all players
        - Opponents
        - Deck
        - Gamedeck
        - Claimed
        - Players' cards, turn
        """
        if self.in_lobby:
            return

        # Opponents
        self.broadcast_opponent_data()

        # Deck
        deck_amount = self.game.deck.get_amount()
        deck_data = {"deck": {"amount": deck_amount}}
        self.sendall(deck_data)

        # Game deck
        gamedeck_amount = self.game.gamedeck.get_amount()
        gamedeck_data = {"game": {"amount": gamedeck_amount}}
        self.sendall(gamedeck_data)

        # Claim data
        claim_rank = self.game.gamedeck.get_last_rank()
        claim_amount = self.game.gamedeck.get_last_amount()
        claim_data = {"game": {"latest": {"amount": claim_amount, "rank": claim_rank}, "duration": None}}
        self.sendall(claim_data)

        # Player data
        self.broadcast_player_data()

        # Allowed claims
        self.broadcast_allowed_claims()

    def broadcast_opponent_data(self):
        """
        Send opponent data to each player
        - Name
        - UID
        - Card amount
        - Turn
        """
        for client in self.clients:
            uid = client.get_uid()
            opponents = []

            for opponent_client in self.clients:
                opponent_uid = opponent_client.get_uid()
                if opponent_uid != uid:
                    player = self.game.turnmanager.get_player(opponent_uid)
                    amount = player.hand.get_amount()
                    turn = self.game.turnmanager.is_in_turn(player) or self.game.turnmanager.is_first_round()
                    played = self.game.last_played_player == player

                    opponents.append({"amount": amount, "name": player.get_name(), "uid": opponent_uid, "turn": turn,
                                      "played": played, "suspected": False})

            opponent_data = {"opponents": opponents}
            self.send(client, opponent_data)

    def broadcast_player_data(self):
        """
        Broadcast each player info
        - Cards
        - Turn
        """
        for client in self.clients:
            player = self.game.turnmanager.get_player(client.get_uid())
            cards = player.hand.get_cards()
            turn = self.game.turnmanager.is_in_turn(player) or self.game.turnmanager.is_first_round()
            player_data = {"player": {"cards": cards, "turn": turn}}
            self.send(client, player_data)

    def broadcast_pause(self):
        """
        Broadcast info that pauses the game
        No one is in turn until broadcasted otherwise
        """
        for client in self.clients:
            uid = client.get_uid()
            player = self.game.turnmanager.get_player(uid)
            opponents = self.game.turnmanager.get_opponents(player)
            opponent_data = []
            for opponent in opponents:
                opponent_uid = opponent.get_uid()
                turn = False
                opponent_data.append({"uid": opponent_uid, "turn": turn})
                self.send(client, {"opponents": opponent_data})

        allowed = []
        denied = {}
        for rank in range(2, 15):
            denied[rank] = 8

        self.sendall({"claimgrid": {"allowed": allowed, "denied": denied}})

    def broadcast_played_cards(self):
        """
        Broadcasts last played cards
        """
        all_cards = self.game.gamedeck.get_cards()
        amount = self.game.gamedeck.get_last_amount()
        cards = all_cards[-amount:]
        self.sendall({"game": {"display": cards}})

    def broadcast_allowed_claims(self):
        """
        Broadcast allowed claims
        If player is not in turn deny all claims
        """
        for client in self.clients:
            player = self.game.turnmanager.get_player(client.get_uid())
            if self.game.turnmanager.is_in_turn(player) or self.game.turnmanager.is_first_round():
                allowed, denied = self.game.get_allowed_claims()
            else:
                allowed = []
                denied = {}
                for rank in range(2, 15):
                    denied[rank] = 8
            self.send(client, {"claimgrid": {"allowed": allowed, "denied": denied}})

    def broadcast_discard(self, duration):
        """
        Broadcast game deck discard's wait duration
        :param duration: float
        """
        self.sendall({"game": {"duration": duration}})

    def broadcast_suspect(self, player_who_suspects):
        """
        Broadcast suspect events
        :param player_who_suspects: Player
        """
        self.broadcast_pause()
        self.broadcast_played_cards()

        for client in self.clients:
            player = self.game.turnmanager.get_player(client.get_uid())
            opponents = self.game.turnmanager.get_opponents(player)

            data = []
            for opponent in opponents:
                uid = opponent.get_uid()
                suspected = opponent == player_who_suspects
                data.append({"uid": uid, "suspected": suspected})
            self.send(client, {"opponents": data})

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
        Get joined players and start the game
        """
        self.in_lobby = False
        players = []
        for client in self.clients:
            client.play()
            players.append((client.get_uid(), client.get_name()))
        self.game = Game(players)
        self.game.start()
        self.broadcast_game()

    def get_player(self, client):
        """
        Get game player by client
        :param client: Client
        :return: Player
        """
        return self.game.turnmanager.get_player(client.get_uid())

    def wait_for_discard(self, wait):
        """
        Start discard waiting (ONLY CALL IN A THREAD)
        Calls discard method after waiting
        :param wait: int, waiting time in seconds
        """
        print(f"Waiting {wait} seconds to discard")
        sleep(wait)
        if not self.is_displaying():
            self.game.discard()
            self.broadcast_game()

    def wait_for_display(self, wait):
        """
        Show display cards for <wait> seconds and continue after
        :param wait: int, seconds
        """
        print(f"Waiting {wait} seconds for displaying")
        sleep(wait)
        self.sendall({"game": {"display": []}})
        self.displaying = False
        self.broadcast_game()

    def is_displaying(self):
        return self.displaying
