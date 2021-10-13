from tkinter import *
from PIL import Image, ImageTk

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
        opponent = Opponent(self, name=name)
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

    def set_turn(self, uid, turn):
        opponent = self.get_opponent(uid)
        opponent.set_turn(turn)

    def set_played(self, uid, played):
        opponent = self.get_opponent(uid)
        opponent.set_played(played)

    def set_suspected(self, uid, suspected):
        opponent = self.get_opponent(uid)
        opponent.set_suspected(suspected)

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


class Opponent(CardPile):

    def __init__(self, parent, name):
        super().__init__(parent, name=name)

        self.indicator_label = Label(self, bg="#35654d")
        self.indicator_label.place(x=106, y=190)
        self.played_img, self.suspected_img, self.turn_img = self.get_images()

        self.played = False
        self.suspected = False
        self.turn = False

    @staticmethod
    def get_images():
        """
        Add images as indicator label's attributes
        :return 3 Images
        """
        played = Image.open("gui/mainwindow/assets/spades.png")
        suspected = Image.open("gui/mainwindow/assets/questionmark.png")
        turn = Image.open("gui/mainwindow/assets/turn_arrow.png")

        return ImageTk.PhotoImage(played), ImageTk.PhotoImage(suspected), ImageTk.PhotoImage(turn)

    def set_turn(self, turn):

        color = "lightgreen" if turn else "white"
        self.name_label.config(fg=color)
        self.amount_label.config(fg=color)

        self.turn = turn
        self.set_image()

    def set_played(self, played):
        self.played = played
        self.set_image()

    def set_suspected(self, suspected):
        self.suspected = suspected
        self.set_image()

    def set_image(self):
        """
        Set image based on status
        """
        if self.suspected:
            image = self.suspected_img
        elif self.turn:
            image = self.turn_img
        elif self.played:
            image = self.played_img
        else:
            image = ''
        self.indicator_label.config(image=image)
