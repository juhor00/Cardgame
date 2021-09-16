try:
    from card import OpenedCard, calculate_size
except ImportError:
    from .card import OpenedCard, calculate_size
from tkinter import *
from PIL import Image, ImageTk, ImageOps
from importlib_resources import files


class Hand(Frame):
    """
    Player's hand widget
    """
    def __init__(self, parent):

        _, card_height = calculate_size()
        self.elevate = 40
        self.width = 584
        super().__init__(parent, width=self.width, height=card_height + self.elevate, bg="#35654d")
        self.parent = parent

        self.cards = []
        self.skip = 0

        self.left_arrow = Button(self, command=self.scroll_down,
                                 relief="flat", bd=0, bg="#35654d", activebackground="#35654d")
        self.right_arrow = Button(self, command=self.scroll_up,
                                  relief="flat", bd=0, bg="#35654d", activebackground="#35654d")

        self.add_arrow_images()

    def add_arrow_images(self):
        """
        Add images to arrow buttons
        """
        try:
            image = Image.open("./assets/arrow.png")
        except FileNotFoundError:
            image = Image.open(files("gui.mainwindow.assets").joinpath("arrow.png"))

        right = image.resize((40, 40), Image.ANTIALIAS)
        left = ImageOps.mirror(right)

        right = ImageTk.PhotoImage(right)
        self.right_arrow.img = right
        self.right_arrow.config(image=right)

        left = ImageTk.PhotoImage(left)
        self.left_arrow.img = left
        self.left_arrow.config(image=left)

    def add_card(self, card_str):
        """
        Adds a new card to hand
        :param card_str: str, XY where X is rank and Y is suit
        """
        rank = card_str[0]
        if rank == "1":
            rank = "10"
            suit = card_str[2]
        else:
            suit = card_str[1]

        card = OpenedCard(self, rank, suit)
        card.config(command=lambda: self.on_click(card))
        card.bind("<MouseWheel>", self.on_scroll)
        self.cards.append(card)
        self.draw()
        if len(self.cards) == 1:
            self.lift()

    def add_cards(self, cards):
        """
        Add multiple cards
        :param cards: list
        """
        for card in cards:
            self.add_card(card)

    def remove_card(self, to_remove):
        """
        Removes a card
        :param to_remove: str
        """
        for index, card in enumerate(self.cards):
            if str(card) == to_remove:
                self.cards.remove(card)
                card.destroy()
                if index >= self.skip:
                    self.skip -= 1
                    if self.skip < 0:
                        self.skip = 0
                break
        self.draw()
        if len(self.cards) == 0:
            self.lower()

    def remove_cards(self, cards):
        """
        Remove multiple cards
        :param cards: list, str
        """
        for card in cards:
            self.remove_card(card)

    def get_cards(self):
        """
        Return all cards in hand
        :return: str list
        """
        cards = []
        for card in self.cards:
            cards.append(str(card))
        return cards

    def draw(self):
        """
        Draw cards
        """
        card_width, card_height = calculate_size()
        card_pad = 40
        amount = len(self.cards)
        if amount > 10:
            amount = 10

        self.cards.sort()
        self.erase()

        first_coordinate = (self.width - card_pad * (amount - 1) - card_width) / 2

        # Cards
        coordinate = None
        for count, index in enumerate(range(self.skip, amount+self.skip)):
            card = self.cards[index]
            coordinate = first_coordinate + (count * card_pad)
            card.place(x=coordinate, y=self.elevate)
            card.lift()

        # Arrows
        arrow_size = 40
        arrow_pad = 20

        if self.skip != 0:
            x = first_coordinate - arrow_size - arrow_pad
            y = self.elevate + card_height / 2 - arrow_size / 2
            self.left_arrow.place(x=x, y=y)

        if coordinate is None:
            return

        if self.skip < len(self.cards) - amount:
            x = coordinate + card_width + arrow_pad
            y = self.elevate + card_height / 2 - arrow_size / 2
            self.right_arrow.place(x=x, y=y)

    def erase(self):
        """
        Erases cards and arrows, does not delete
        """
        for card in self.cards:
            card.place_forget()

        self.left_arrow.place_forget()
        self.right_arrow.place_forget()

    def on_click(self, card: OpenedCard):
        """
        Emit virtual event if card was elevated
        """
        if card.elevated:
            self.event_generate("<<Card-clicked>>", data={"content": str(card)})

    def on_scroll(self, event):
        """
        Scroll action
        :param event: tkinter event
        """

        # Scroll down
        if not self.is_skippable():
            return
        if event.delta < 0:
            self.scroll_down()
        # Scroll up
        else:
            self.scroll_up()

    def scroll_up(self):
        """
        Scroll cards to right
        """
        self.skip += 1
        max_skip = self.max_skip()
        if self.skip > max_skip:
            self.skip = max_skip
        for card in self.cards:
            card.on_leave()
        self.draw()

    def scroll_down(self):
        """
        Scroll cards to left
        """
        self.skip -= 1
        if self.skip < 0:
            self.skip = 0
        for card in self.cards:
            card.on_leave()
        self.draw()

    def is_skippable(self):
        """
        Return True if cards can be skipped on hand
        :return: bool
        """
        amount = len(self.cards)
        max_cards = 10
        return amount > max_cards

    def max_skip(self):
        """
        Return amount of cards that can be skipped from the beginning
        :return: int
        """
        amount = len(self.cards)
        max_cards = 10
        return amount - max_cards


if __name__ == "__main__":
    root = Tk()
    hand = Hand(root)
    hand.add_cards(["2C", "10D", "AH", "QS", "7C", "7D", "9H", "KS", "2S", "3D", "4D", "9S"])
    hand.grid()
    root.mainloop()
