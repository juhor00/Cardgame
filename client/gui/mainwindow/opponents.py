from tkinter import *

try:
    from .cardpile import CardPile
except ImportError:
    from cardpile import CardPile


class Opponents(Frame):
    """
    Frame in which all opponents are shown
    """
    def __init__(self, parent):
        super().__init__(parent, width=1280, height=234, bg="#35654d")
        self.parent = parent

        self.opponents = {}

    def add(self, uid, name, amount=0):
        """
        Add an opponent
        :param uid: int
        :param name: str
        :param amount: int
        """
        opponent = CardPile(self, name=name)
        opponent.set_amount(amount)
        self.opponents[uid] = opponent
        self.draw()

    def remove_opponent(self, uid):
        """
        Remove an opponent
        :param uid: int
        """
        del self.opponents[uid]
        self.draw()

    def set_amount(self, uid, amount):
        """
        Set opponent's card amount
        :param uid: int
        :param amount: int
        """
        opponent = self.get_opponent(uid)
        opponent.set_amount(amount)

    def set_name(self, uid, name):
        opponent = self.get_opponent(uid)
        opponent.set_name(name)

    def get_opponent(self, uid):
        return self.opponents[uid]

    def draw(self):
        """
        Draws all opponents
        """
        if len(self.opponents) == 0:
            return
        self.update()

        keys = list(self.opponents.keys())

        pile_width = self.opponents[keys[0]].winfo_reqwidth()
        width = self.winfo_reqwidth()
        offset = 100

        first_coordinate = (width - (offset + pile_width) * (len(self.opponents) - 1) - pile_width) / 2
        for index, uid in enumerate(self.opponents):
            opponent = self.opponents[uid]
            x = first_coordinate + (index * (offset + pile_width))
            opponent.place(x=x, y=0)
