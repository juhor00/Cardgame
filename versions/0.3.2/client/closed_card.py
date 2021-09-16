from tkinter import *
from PIL import Image, ImageTk
from card import calculate_size


class Card(Label):

    def __init__(self, master):
        self.image = None
        super().__init__(master)
        self.add_image()

    def add_image(self):
        """
        Adds an image to the card
        """
        image = Image.open(f"assets/cards/red_back.png")

        # Resize
        image = image.resize(calculate_size(), Image.ANTIALIAS)

        # Add image to card
        image = ImageTk.PhotoImage(image)
        self.image = image
        self.config(image=image)
