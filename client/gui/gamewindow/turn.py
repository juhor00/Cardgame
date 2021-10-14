from tkinter import *
from PIL import Image, ImageTk


class Turn(Label):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        image = Image.open("gui/gamewindow/assets/your_turn.png")
        self.image = ImageTk.PhotoImage(image)
        self.config(image=image)

    def hide(self):
        self.config(image="")

    def show(self):
        self.config(image=self.image)
