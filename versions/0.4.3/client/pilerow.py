import cardpile
from tkinter import Frame


class Row(Frame):

    def __init__(self, master, height):
        """
        A row of cardpiles such as deck
        :param master: widget parent
        """
        super().__init__(master)
        self.height = height
        self.master = master
        self.width = self.master.winfo_width()

    def place_row(self, x, y):
        """
        Places the row on coordinates x, y
        Width is as wide as master
        :param x: int
        :param y: int
        """
        self.place(x=x, y=y)
