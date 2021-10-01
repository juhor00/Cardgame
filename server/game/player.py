import game.deck as deck
from game.card import Card


class Player:

    def __init__(self, name, player_id):
        """
        Create a player
        :param name: str
        :param player_id: int
        """

        self.name = name
        self.id = player_id
        self.hand = deck.Deck()

    def __str__(self):
        return self.name

    def get_name(self):
        return str(self)

    def get_id(self):
        return self.id

    def print(self):
        print(self)
        self.hand.print()

    def add(self, card):
        self.hand.add(card)