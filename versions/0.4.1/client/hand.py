from card import OpenedCard, calculate_size
from tkinter import Frame


class Hand(Frame):

    def __init__(self, master, settings):
        super().__init__(master)

        self.master = master
        self.cards = []
        self.settings = settings
        #
        self.place(x=0,y=0,width=0,height=0)
        self.config(bg=self.settings["green"])

    def on_click(self, card: OpenedCard):
        """
        Emit virtual event if card was elevated
        """
        if card.elevated:
            self.event_generate("<<Card-clicked>>", data={"content": str(card)})

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
        self.cards.append(card)

    def draw_cards(self):
        """
        Draws player's cards in hand
        """

        frame_width = self.master.winfo_width()       # Width of frame
        card_width = calculate_size()[0]    # Width of a card
        card_pad = int(self.settings["card_padx"])
        first_coordinate = (frame_width - card_pad * (len(self.cards) - 1)
                            - card_width) / 2

        for n, card in enumerate(self.cards):
            coordinate = first_coordinate + (n * card_pad)
            card.place(x=coordinate, y=int(self.settings["card_pady"]))
            card.lift()