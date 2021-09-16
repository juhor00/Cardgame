class Card:

    def __init__(self, param, param2=None):
        """
        Initialize card by string representation or suit and rank
        :param param: str, string representation or only rank
        :param param2: str (suit only) or None
        """
        if param2 is None:
            self.rank_str = param[0]
            self.rank, self.suit = self.card_from_str(param)

        else:
            self.rank_str = param
            self.rank = self.rank_to_int(param)
            self.suit = param2

    def __str__(self):
        """
        Return string representation of card
        :return: str
        """
        return f"{self.rank_str}{self.suit}"

    def __lt__(self, card):
        return self.rank < card.rank

    def __le__(self, card):
        return self.rank <= card.rank

    def __gt__(self, card):
        return self.rank > card.rank

    def __ge__(self, card):
        return self.rank >= card.rank

    def __eq__(self, card):
        return self.rank == card.rank

    def __ne__(self, card):
        return self.rank != card.rank

    def get_rank(self):
        """
        Return rank value
        :return: int
        """
        return self.rank

    @staticmethod
    def card_from_str(param):
        """
        Get suit and rank from string representation
        :param param: str
        :return: str, int tuple
        """
        if len(param) == 2:
            suit, rank = param
            rank = Card.rank_to_int(rank)
        else:
            suit = param[0, 2]
            rank = Card.rank_to_int(param[-1])
        return suit, rank

    @staticmethod
    def rank_to_int(rank):
        """
        Returns integer value of str rank
        :param rank: str, 2-10 or J, Q, K, A
        :return: int, 2-14
        """
        values = {"J": 11,
                  "Q": 12,
                  "K": 13,
                  "A": 14}
        if rank in values:
            return values[rank]
        else:
            return int(rank)