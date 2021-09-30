from game import Game


class Interface:
    """
    Command line input interface for cardgame
    """
    def __init__(self):

        self.game = Game(self.create_players())
        self.game.start()

    def mainloop(self):
        """
        Mainloop of interface
        """
        while len(self.game.turnmanager.get_players()) > 1:
            self.game.print()
            print("Actions: [P] play cards, [S] suspect, [D] play deck card")
            action = input("What action is done? ")
            if action.upper() == "P":
                interface.play_cards()
            elif action.upper() == "S":
                interface.suspect()
            elif action.upper() == "D":
                interface.play_deck()

    @staticmethod
    def create_players():
        """
        Creates players
        Only for offline version
        :return: list tuples (int, str)
        """
        players = []
        for index in range(int(input("How many players? "))):
            name = "Player " + str(index)
            players.append((index, name))
        return players

    def get_player(self):
        """
        Get player by input
        :return: int, id
        """
        while True:
            self.game.turnmanager.print()
            name = input("Insert name: ")

            if name not in self.game.turnmanager.get_names():
                print("Error: Player not found")
                continue
            else:
                return self.game.turnmanager.get_player(name)

    def play_cards(self):
        """
        Ask for player and play cards
        :return: bool, success
        """
        while True:
            print("In turn:", self.game.turnmanager.get_active_player())
            player = self.get_player()
            if player == self.game.turnmanager.get_active_player():
                break
            else:
                print("Error: player must be in turn")

        while True:
            print("Cards in hand: ", end="")
            player.print()
            card_data = input("Pick cards separated by space: ")
            cards = []
            for card in card_data.split():
                if player.hand.has_card(card):
                    cards.append(card)
            if not self.game.correct_amount_of_cards(cards):
                print("Incorrect amount of cards")
                continue

            while True:
                claim = input("Claim cards (2-14): ")
                try:
                    claim = int(claim)
                    break
                except TypeError:
                    print("Error: not integer")

            if not self.game.is_allowed_play(cards, claim):
                print("Error: that play was not allowed!")
                continue
            else:
                return self.game.play(player, cards, claim)

    def suspect(self):
        """
        Ask for player and suspect cards
        """
        while True:
            print("Choose player who suspects")
            player = self.get_player()
            if player == self.game.last_played_player:
                print("Error: player who suspects can't be the one who played cards")
            else:
                break
        self.game.suspect(player)

    def play_deck(self):
        """
        Ask for player and play deck top card
        """
        pass


if __name__ == "__main__":

    interface = Interface()
    interface.mainloop()

