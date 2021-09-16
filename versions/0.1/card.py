from tkinter import *
from PIL import ImageTk, Image

SIZE = (128, 128)   # Max size for each dimension


def calculate_size():
    """
    Calculates the size of the images
    :return: int tuple, (w, h)
    """
    image = Image.open(f"assets/red_back.png")
    ratio = calculate_ratio(SIZE, image.size)
    size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return size


def calculate_ratio(max_size, current_size):
    """
    Calculates resize ratio
    :param max_size: int tuple, (w, h)
    :param current_size: int tuple, (w, h)
    :return: float, ratio
    """
    ratio = min(max_size[0]/current_size[0], max_size[1]/current_size[1])
    return ratio


class Card(Button):

    def __init__(self, master, rank, suit):
        super().__init__(master)
        self.suit_ = str(suit).capitalize()
        self.rank_str_ = str(rank)
        self.rank_ = self.rank_to_int(rank)
        self.add_image()

    def add_image(self):
        """
        Adds an image to the card
        """
        image = Image.open(f"assets/{self.rank_str_}{self.suit_}.png")

        # Resize
        image = image.resize(calculate_size(), Image.ANTIALIAS)

        # Add image to card
        image = ImageTk.PhotoImage(image)
        self.image = image
        self.config(image=image)

    def __str__(self):
        return f"{self.rank_str_}{self.suit_}"


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