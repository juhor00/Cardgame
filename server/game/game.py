
from game.player import Player
from game.deck import Deck, GameDeck
from game.turn import TurnManager


class Game:

    def __init__(self, names):
        """
        Create a game to given players
        :param names: list of tuples (int, str)
        """
        players = []
        for player_id, name in names:
            players.append(Player(name, player_id))

        self.deck = Deck()
        self.gamedeck = GameDeck()
        self.turnmanager = TurnManager(players)
        self.last_played_player = self.turnmanager.get_active_player()

    def start(self):
        """
        Start the game
        Draw 5 cards to all
        Handle first card play
        """
        self.deck.empty()
        self.gamedeck.empty()

        self.deck.generate_cards()
        self.deck.shuffle()
        for player in self.turnmanager.get_players():
            self.draw_cards(self.deck, player, 5)

    def print(self):
        """
        Print current game state
        """
        print("Players:")
        for player in self.turnmanager.get_players():
            print(f" {player} [{player.hand.get_amount()}]", end="")
            if self.turnmanager.get_active_player() == player:
                print(" *")
            else:
                print()
        print(f"Deck [{self.deck.get_amount()}]")
        print(f"Gamedeck [{self.gamedeck.get_amount()}]")
        print(f"Last played: [{self.gamedeck.get_last_rank()}] x{self.gamedeck.get_last_amount()}")

    def play(self, player, cards, claim):
        """
        Play cards
        :param player: Player
        :param cards: list of str
        :param claim: int
        :return: bool
        """

        for card in cards:
            if not player.hand.has_card(card):
                print(f"Player {player} doesn't have card {card}. Hand: {player.hand.get_cards()}")
                return False
        if not self.is_allowed_play(cards, claim):
            print(f"Claim {claim} not allowed. Card amount was {len(cards)}")
            return False

        # These claims can be only played 1 card at a time
        if claim in [2, 10, 14]:
            if len(cards) > 1:
                print(f"Only 1 card can be played when claiming {claim}. {player} played {len(cards)} cards.")
                return False

        # First round anyone can play
        if self.turnmanager.is_first_round():
            self.turnmanager.turn_to(player.get_name())

        # Check if is allowed to play
        else:
            if not player == self.turnmanager.get_active_player():
                print(f"Player {player} is not in turn and is not allowed to play. "
                      f"In turn: {self.turnmanager.get_active_player()}")
                return False

        # Player who played last won
        if self.last_played_player.hand.is_empty():
            print(self.last_played_player, "won!")

        # Play cards
        self.gamedeck.add_multiple(cards)
        self.gamedeck.claim(claim)
        player.hand.remove_multiple(cards)
        self.draw_to_five()
        self.last_played_player = player
        self.turnmanager.change_turn()

    def suspect(self, player):
        """
        Suspecting action
        :param player: Player, who suspects
        :return: bool
        """
        if self.gamedeck.is_empty():
            return False

        claimer = self.last_played_player

        if claimer == player:
            return False

        if self.gamedeck.lied():
            # Player who claimed the cards draw all
            # Player who suspected gets the turn

            self.draw_all(self.gamedeck, claimer)
            self.turnmanager.turn_to(player.get_name())
            print(f"Lied! {claimer} draws all cards and turn jumps to {player}")
        else:
            # Player who suspected draw all
            # Player who claimed keeps the turn
            self.draw_all(self.gamedeck, player)
            print(f"Didn't lie! {player} draws all cards and turn stays")
            self.turnmanager.turn_to(claimer.get_name())
        return True

    def can_suspect(self, player):
        """
        Return True if player is allowed to suspect
        :param player: Player
        :return: bool
        """
        return player != self.last_played_player

    def deck_play(self, player):
        """

        :param player:
        :return:
        """

    def discard(self):
        """
        Discard game deck and turn stays to the player who last played
        Only discard_wait should call this method
        """
        if self.gamedeck.to_discard():
            self.gamedeck.empty()
            self.turnmanager.turn_to(self.last_played_player.get_name())
            print("Discarded")

    def handle_win(self):
        """
        Check if active player has won and remove them from the game
        """
        if self.deck.is_empty():
            if self.turnmanager.get_active_player().hand.is_empty():
                print(f"{self.turnmanager.get_active_player()} has won!")
                self.turnmanager.force_next_turn()

    def draw_all(self, source: Deck, player: Player):
        """
        Draws all cards from source
        :param source: Deck
        :param player: Player
        """
        self.draw_cards(source, player, source.get_amount())
        source.empty()

    def draw_to_five(self):
        """
        Draw cards until active player has 5 cards in hand
        """
        player = self.turnmanager.get_active_player()
        source = self.deck
        amount = 5 - player.hand.get_amount()
        if amount <= 0:
            return
        self.draw_cards(source, player, amount)

    @staticmethod
    def draw_cards(source: Deck, player: Player, amount):
        """
        Draw cards from source to dest (from top)
        :param source: Deck
        :param player: Player
        :param amount: int
        """
        for _ in range(amount):
            if not source.is_empty():
                card = source.get_top()
                player.add(card)
            else:
                break

    def is_allowed_play(self, cards, claim):
        """
        Return True if cards are allowed to be played
        :param cards: list of str
        :param claim: int, claimed rank
        :return: bool
        """
        allowed, reason = self.is_allowed_rank(claim)
        if not allowed:
            print(f"Error: Invalid claim")
            return False
        if not self.correct_amount_of_cards(cards):
            print("Error: Invalid amount of cards")
            return False

        return True

    def is_allowed_rank(self, rank):
        """
        Return tuple (bool, int), If allowed, return True, 0
        Else return False and reason ID (int)
        Reasons are in data_structure.txt
        :param rank: int
        :return: bool, int
        """
        # Empty gamedeck
        if self.gamedeck.get_last_rank() is None:
            if rank == 10 or rank == 14:
                return False, 1
            if not self.deck.is_empty():
                if rank > 10:
                    return False, 2
            return True, 0

        if rank == 2:
            return True, 0
        if rank < self.gamedeck.get_last_rank():
            return False, 3
        if self.gamedeck.get_last_rank() == 2:
            return False, 4
        if rank == 10:
            if self.gamedeck.get_last_rank() > 9:
                return False, 5
        if rank == 14:
            if self.gamedeck.get_last_rank() < 11:
                return False, 6
        if self.gamedeck.get_last_rank() < 7:
            if 11 <= rank <= 13:
                return False, 7

        return True, 0

    def correct_amount_of_cards(self, cards):
        """
        Return True if the amount of cards is allowed
        :param cards: list
        :return: bool
        """
        if self.gamedeck.get_last_rank() == 2:
            if len(cards) == 1:
                return True
            else:
                return False

        if len(cards) > 4:
            return False

        if len(cards) == 0:
            return False

        return True

    def get_allowed_claims(self):
        """
        Return list of allowed and dict of denied claims
        :return: list of int, dict of int: str
        """
        allowed = []
        denied = {}
        for rank in range(2, 15):
            is_allowed, reason = self.is_allowed_rank(rank)
            if is_allowed:
                allowed.append(rank)
            else:
                denied[rank] = reason

        return allowed, denied
