from game.card import *
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

    def remove_multiple(self, cards):
        """
        Remove multiple cards
        :param cards: list of str
        """
        for card in cards:
            self.remove(Card(card))

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
        if type(card) == Card:
            return card in self.cards
        # String
        else:
            for c in self.cards:
                if card == str(c):
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
        print(f" [{len(self.cards)}]")
        for card in sorted(self.cards):
            print(f" {card}")

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.seed(time.time())
        random.shuffle(self.cards)

    def get_cards(self):
        """
        Return cards in str format
        :return: list of str
        """
        cards = []
        for card in self.cards:
            cards.append(str(card))
        return cards


class GameDeck(Deck):

    def __init__(self):
        super().__init__()
        self.last_amount = 0
        self.claimed = []

    def add_multiple(self, cards):
        """
        Add cards to claimed cards
        :param cards: list of cards
        """
        for card in cards:
            if type(card) == str:
                card = Card(card)
            super().add(card)
        self.last_amount = len(cards)

    def claim(self, rank):
        """
        Add claimed cards
        :param rank: int
        """
        for _ in range(self.last_amount):
            self.claimed.append(rank)

    def get_last_rank(self):
        """
        Return last rank
        :return: int, 2-14
        """
        if len(self.claimed) == 0:
            return None
        return self.claimed[-1]

    def get_last_amount(self):
        """
        Return last amount
        :return: int
        """
        return self.last_amount

    def to_discard(self):

        if self.is_empty():
            return False

        rank = self.get_last_rank()

        # 10 or Ace
        if rank == 10 or rank == 14:
            return True

        # Never discard when playing 2's
        if rank == 2:
            return False

        if len(self.cards) < 4:
            return False

        claimed = self.claimed[::-1]
        for i in range(4):
            card = claimed[i]
            if card != rank:
                # Not 4 same cards
                return False
        # 4 same cards
        return True

    def lied(self):
        """
        Return True if last played cards were lied
        :return: bool
        """
        claimed = self.claimed[::-1]
        cards = self.cards[::-1]
        for i in range(self.last_amount):
            claim = claimed[i]
            actual = cards[i]
            if actual.get_rank() != claim:
                return True
        return False

    def empty(self):
        super().empty()
        self.claimed = []
        self.last_amount = 0
