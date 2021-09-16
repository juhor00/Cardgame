from card import *
import random
import time


class Deck:
    """
    A data structure for a generic deck
    """

    def __init__(self):

        self.cards = []

    def add(self, card):
        """
        Add a card
        :param card: Card
        """
        self.cards.append(card)

    def remove(self, card):
        """
        Remove a card
        :param card: Card
        """
        self.cards.remove(card)

    def is_empty(self):
        """
        Return True if there are no cards
        :return: bool
        """
        return len(self.cards) == 0

    def get_amount(self):
        """
        Return the amount of cards
        :return: int
        """
        return len(self.cards)

    def get_top(self):
        """
        Remove top card and return it
        :return: Card
        """
        card = self.cards.pop(-1)
        return card

    def has_card(self, card):
        """
        Return True if card is in deck
        :param card: Card instance or string
        :return: bool
        """
        # Card instance
        if type(card) == card.Card:
            return card in self.cards
        # String
        else:
            for c in self.cards:
                if card == c.to_str():
                    return True
            return False

    def generate_cards(self):
        """
        Generates all cards to deck
        """
        for index in range(52):
            if index < 52 * 1 / 4:
                suit = "C"
            elif index < 52 * 2 / 4:
                suit = "D"
            elif index < 52 * 3 / 4:
                suit = "H"
            else:
                suit = "S"

            rank = index % 13 + 2
            if rank == 11:
                rank = "J"
            elif rank == 12:
                rank = "Q"
            elif rank == 13:
                rank = "K"
            elif rank == 14:
                rank = "A"
            card = Card(rank, suit)
            self.add(card)

    def empty(self):
        self.cards = []

    def print(self):
        print(f"[{len(self.cards)}]")
        for card in self.cards:
            print(card)

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.seed(time.time())
        random.shuffle(self.cards)

