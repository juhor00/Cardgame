import game.deck as deck
from game.card import Card


class Player:

    def __init__(self, name, uid):
        """
        Create a player
        :param name: str
        :param uid: int
        """

        self.name = name
        self.uid = uid
        self.hand = deck.Deck()

    def __str__(self):
        return self.name

    def get_name(self):
        return str(self)

    def get_uid(self):
        return self.uid

    def print(self):
        print(self)
        self.hand.print()

    def add(self, card):
        self.hand.add(card)
