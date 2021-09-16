from card import OpenedCard, calculate_size
from tkinter import Frame, Button
from PIL import Image, ImageTk, ImageOps


class Hand(Frame):

    def __init__(self, master, settings):
        super().__init__(master)

        self.master = master
        self.cards = []
        self.settings = settings
        self.start_card = 0

        self.place(x=0, y=0, width=0, height=0)
        self.config(bg=self.settings["green"])

        self.left_arrow = Button(master, bg=self.settings["green"], relief="flat")
        self.right_arrow = Button(master, bg=self.settings["green"], relief="flat")
        self.left_arrow.config(command=self.scroll_down)
        self.right_arrow.config(command=self.scroll_up)

        self.arrow_w = int(self.settings["arrow_width"])
        self.arrow_h = int(self.settings["arrow_height"])
        self.add_arrow_images()

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
        self.start_card += 1
        max_skip = self.max_skip()
        if self.start_card > max_skip:
            self.start_card = max_skip
        for card in self.cards:
            card.on_leave()
        self.draw_cards()

    def scroll_down(self):
        """
        Scroll cards to left
        """
        self.start_card -= 1
        if self.start_card < 0:
            self.start_card = 0
        for card in self.cards:
            card.on_leave()
        self.draw_cards()

    def add_arrow_images(self):
        """
        Adds arrows
        """
        image = Image.open("assets/arrow.png")
        right = image.resize((self.arrow_w, self.arrow_h), Image.ANTIALIAS)
        left = ImageOps.mirror(right)

        right = ImageTk.PhotoImage(right)
        self.right_arrow.img = right
        self.right_arrow.config(image=right)

        left = ImageTk.PhotoImage(left)
        self.left_arrow.img = left
        self.left_arrow.config(image=left)

    def add_cards(self, data):
        """
        Add new cards to hand
        :param data: list of str
        """
        for card in data:
            self.add_card(card)

        self.draw_cards()

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

        card = OpenedCard(self.master, rank, suit)
        card.config(command=lambda: self.on_click(card))
        card.bind("<MouseWheel>", self.on_scroll)
        self.cards.append(card)

    def draw_cards(self):
        """
        Draws player's cards in hand
        """

        frame_width = self.master.winfo_width()
        card_width, card_height = calculate_size()
        card_padx = int(self.settings["card_padx"])
        card_pady = int(self.settings["card_pady"])
        arrow_pad = int(self.settings["arrow_pad"])
        amount = len(self.cards)
        start = self.start_card
        if amount > 10:
            amount = 10
        first_coordinate = (frame_width - card_padx * (amount - 1)
                            - card_width) / 2
        self.cards.sort()

        for card in self.cards:
            card.place_forget()

        self.left_arrow.place_forget()
        self.right_arrow.place_forget()

        # Cards
        coordinate = None
        for n, index in enumerate(range(start, amount+start)):
            card = self.cards[index]
            coordinate = first_coordinate + (n * card_padx)
            card.place(x=coordinate, y=card_pady)
            card.lift()

        # Left arrow
        if self.start_card != 0:
            x = first_coordinate - self.arrow_w - arrow_pad
            y = card_pady + card_height / 2 - self.arrow_h / 2
            self.left_arrow.place(x=x, y=y)

        if coordinate is None:
            return
        # Right arrow
        if self.start_card < len(self.cards) - amount:
            x = coordinate + card_width + arrow_pad
            y = card_pady + card_height / 2 - self.arrow_h / 2
            self.right_arrow.place(x=x, y=y)

    def max_skip(self):
        """
        Return amount of cards that can be skipped from the beginning
        :return: int
        """
        amount = len(self.cards)
        max_cards = int(self.settings["max_hand_cards"])
        return amount - max_cards

    def is_skippable(self):
        """
        Return True if cards can be skipped on hand
        :return: bool
        """
        amount = len(self.cards)
        max_cards = int(self.settings["max_hand_cards"])
        return amount > max_cards
