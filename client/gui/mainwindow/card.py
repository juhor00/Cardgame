from tkinter import *
from PIL import ImageTk, Image
from importlib_resources import files


def calculate_size():
    """
    Calculates the size of the images
    :return: int tuple, (w, h)
    """
    try:
        image = Image.open("./assets/cards/red_back.png")
    except FileNotFoundError:
            image = Image.open(files("gui.mainwindow.assets.cards").joinpath("red_back.png"))

    size = (160, 160)
    ratio = calculate_ratio(size, image.size)
    size = (round(image.size[0] * ratio), round(image.size[1] * ratio))
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


class OpenedCard(Button):

    def __init__(self, master, rank, suit):
        self.image = None
        super().__init__(master)
        self.suit_ = str(suit).capitalize()
        self.rank_str_ = str(rank)
        self.rank_ = self.rank_to_int(rank)
        self.add_image()
        self.elevated = False
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Motion>", self.on_enter)
        self.update()
        self.elevated_y = None
        self.normal_y = None
        self.config(bd=0, highlightthickness=0)

        width, height = calculate_size()
        self.config(width=width, height=height)

    def add_image(self):
        """
        Adds an image to the card
        """
        try:
            image = Image.open(f"./assets/cards/{self.rank_str_}{self.suit_}.png")
        except FileNotFoundError:
            image = Image.open(files("gui.mainwindow.assets.cards").joinpath(f"{self.rank_str_}{self.suit_}.png"))

        # Resize
        image = image.resize(calculate_size(), Image.ANTIALIAS)

        # Add image to card
        image = ImageTk.PhotoImage(image)
        self.image = image
        self.config(image=image)

    def __str__(self):
        return f"{self.rank_str_}{self.suit_}"

    def __lt__(self, other):
        return self.rank_ < other.rank_

    def on_enter(self, event):
        """
        Elevate the card when hovered over
        """
        if self.elevated:
            return

        _, h = calculate_size()
        elevate = 40
        if event.y >= h - elevate:
            return

        if self.elevated_y is None or self.normal_y is None:
            y = self.winfo_y()
            self.elevated_y = y - elevate
            self.normal_y = y

        self.elevated = True
        self.place(y=self.elevated_y)

    def on_leave(self, event=None):
        """
        Lowers the card when not hovered over anymore
        """
        if not self.elevated:
            return

        self.elevated = False
        self.place(y=self.normal_y)

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


class ClosedCard(Label):

    def __init__(self, master):
        self.image = None
        super().__init__(master)
        self.add_image()
        self.config(bd=0)

        width, height = calculate_size()
        self.config(width=width, height=height)

    def add_image(self):
        """
        Adds an image to the card
        """
        try:
            image = Image.open("./assets/cards/red_back.png")
        except FileNotFoundError:
            image = Image.open(files("gui.mainwindow.assets.cards").joinpath("red_back.png"))

        # Resize
        image = image.resize(calculate_size(), Image.ANTIALIAS)

        # Add image to card
        image = ImageTk.PhotoImage(image)
        self.image = image
        self.config(image=image)


if __name__ == "__main__":
    root = Tk()
    closed = ClosedCard(root)
    closed.pack()
    root.mainloop()