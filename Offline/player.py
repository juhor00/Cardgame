import deck
from card import Card


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

    def play_card(self):
        card_list = []
        while True:
            self.print()
            cards = input("Choose cards, separated by space: ")
            for card in cards.split():
                if self.hand.has_card(card):
                    card_list.append(Card(card))
                    if len(card_list) > 4:
                        print("Too many cards, max is 4")
                        card_list = []
                        break
                else:
                    print(f"Unknown card {card}")
                    card_list = []
                    break
            if len(card_list) == 0:
                continue
            for card in card_list:
                self.hand.remove(card)
            return card_list
