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

    def play_cards(self):
        """
        Asks the player to play the cards
        """
        cards = []
        while not self.correct_amount_of_cards(cards):
            cards = self.turnmanager.get_active_player().play_card()
        self.gamedeck.add_multiple(cards)
        self.gamedeck.print()

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