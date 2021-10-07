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

        self.opponents = []

    def add(self, uid, name, amount=0):
        """
        Add an opponent
        :param uid: int
        :param name: str
        :param amount: int
        """
        opponent = CardPile(self, name=name, uid=uid)
        opponent.set_amount(amount)
        self.opponents.append(opponent)
        self.draw()

    def remove_opponent(self, name):
        """
        Remove an opponent
        :param name: str
        """
        for opponent in self.opponents:
            if str(opponent) == name:
                self.opponents.remove(opponent)
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
        for opponent in self.opponents:
            if opponent.get_uid() == uid:
                return opponent

    def draw(self):
        """
        Draws all opponents
        """
        if len(self.opponents) == 0:
            return
        self.update()
        pile_width = self.opponents[0].winfo_reqwidth()
        width = self.winfo_reqwidth()
        offset = 100

        first_coordinate = (width - (offset + pile_width) * (len(self.opponents) - 1) - pile_width) / 2
        for index, opponent in enumerate(self.opponents):
            x = first_coordinate + (index * (offset + pile_width))
            opponent.place(x=x, y=0)