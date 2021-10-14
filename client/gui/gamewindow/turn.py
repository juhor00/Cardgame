from tkinter import *
from PIL import Image, ImageTk


class Turn(Label):

    def __init__(self, parent):
        super().__init__(parent, bd=0, bg=parent["bg"])
        self.parent = parent
        image = Image.open("gui/gamewindow/assets/your_turn.png")
        image = image.resize((232, 113), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)

    def hide(self):
        self.config(image="")

    def show(self):
        self.config(image=self.image)
