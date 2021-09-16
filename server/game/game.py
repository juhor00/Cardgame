try:
    from .player import Player
    from .deck import Deck, GameDeck
    from .turn import TurnManager
except ImportError:
    from player import Player
    from deck import Deck, GameDeck
    from turn import TurnManager


class Game:

    def __init__(self):
        self.deck = Deck()
        self.gamedeck = GameDeck()
        self.turnmanager = TurnManager()

    def game_handler(self):
        """
        Handle game events
        """

        self.start()

        while len(self.turnmanager.get_players()) > 1:

            self.handle_suspect()

            self.handle_remove()

            self.handle_win()

            self.turnmanager.change_turn()

            self.play_cards()

            self.claim()

            self.draw_to_five()

    def start(self, players):
        """
        Start the game
        Draw 5 cards to all
        Handle first card play
        :param players: list of str
        """
        self.deck.empty()
        self.gamedeck.empty()

        self.deck.generate_cards()
        self.deck.shuffle()

        self.turnmanager.create_players(players)
        for player in self.turnmanager.get_players():
            self.draw_cards(self.deck, player, 5)

        #self.play_first_card()
        #self.draw_to_five()

    def play_first_card(self):
        """
        Lets any player play the first card
        """
        while True:

            for player in self.turnmanager.get_players():
                player.print()
            name = input("Who starts? Insert name: ")

            if name not in self.turnmanager.get_names():
                print("Error: Player not found")
                continue
            else:
                break

        while name != self.turnmanager.get_active_player().name:
            self.turnmanager.change_turn()
        self.play_cards()
        self.claim(3)
        return

    def handle_suspect(self):
        """
        Asks if anyone wants to suspect and handle suspects
        """
        while True:
            answer = input("Does anyone want to suspect? (y/n): ").lower()
            print(answer)
            # Suspect
            if answer == "y":
                suspect_player = None
                while suspect_player is None:
                    self.turnmanager.print_others()
                    suspect_name = input("Who suspects? (name): ")
                    suspect_player = self.turnmanager.get_player(suspect_name)
                    if suspect_player is not None:
                        self.suspect(suspect_player)
                    else:
                        print("Error: Player not found")
                return
            elif answer == "n":
                return
            else:
                print("Error: Command not found")

    def suspect(self, player):
        """
        Suspecting action
        """
        if self.gamedeck.lied():
            # Player who claimed the cards draw all
            # Player who suspected gets the turn
            claimer = self.turnmanager.get_active_player()
            self.draw_all(self.gamedeck, claimer)
            self.turnmanager.turn_to(player.get_name())
            print(f"Lied! {claimer} draws all cards and turn jumps to {player}")
        else:
            # Player who suspected draw all
            # Player who claimed keeps the turn
            self.draw_all(self.gamedeck, player)
            print(f"Didn't lie! {player} draws all cards and turn stays")
        self.turnmanager.stay_next_turn()
                
    def handle_remove(self):
        """
        Discard cards from gamedeck if needed
        """
        if self.gamedeck.to_discard():
            self.gamedeck.empty()
            self.turnmanager.stay_next_turn()

    def handle_win(self):
        """
        Check if active player has won and remove them from the game
        """
        if self.deck.is_empty():
            if self.turnmanager.get_active_player().hand.is_empty():
                print(f"{self.turnmanager.get_active_player()} has won!")
                self.turnmanager.force_next_turn()

    def play_cards(self):
        """
        Asks the player to play the cards
        """
        cards = []
        while not self.correct_amount_of_cards(cards):
            cards = self.turnmanager.get_active_player().play_card()
        self.gamedeck.add_multiple(cards)
        self.gamedeck.print()

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

    def claim(self, forced_claim=None):
        """
        Asks the player to claim the cards
        """

        if forced_claim is not None:
            self.gamedeck.claim(forced_claim)
            return

        allowed = []
        for rank in range(2, 15):
            if self.is_allowed_rank(rank):
                allowed.append(rank)

        while True:
            print(f"Allowed claims: {allowed}")
            rank = int(input("Claim: "))

            if rank in allowed:
                self.gamedeck.claim(rank)
                return

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

    def is_allowed_rank(self, rank):
        """
        Return True if rank is allowed
        :param rank: int
        :return: bool
        """
        # Empty gamedeck
        if self.gamedeck.get_last_rank() is None:
            if rank == 10 or rank == 14:
                return False
            if not self.deck.is_empty():
                if rank > 10:
                    return False
            return True

        if rank == 2:
            return True
        if rank < self.gamedeck.get_last_rank():
            return False
        if self.gamedeck.get_last_rank() == 2:
            return False
        if rank == 10:
            if self.gamedeck.get_last_rank() > 9:
                return False
        if rank == 14:
            if self.gamedeck.get_last_rank() < 11:
                return False
        if self.gamedeck.get_last_rank() < 7:
            if 11 <= rank <= 13:
                return False
        if rank == 10 or rank == 14:
            if self.deck.is_empty():
                return False
        if rank > 10 and self.gamedeck.get_last_rank() is None:
            if not self.deck.is_empty():
                return False

        return True


    def get_hand(self, id):
        """
        Get cards of player ID
        :param id: int
        :return:
        """

    def print(self):
        """
        Print game status
        """
        print("Game status")
        self.turnmanager.print()
        print("Deck: ", end="")
        self.deck.print_amount()
        print("Game: ", end="")
        self.gamedeck.print_amount()