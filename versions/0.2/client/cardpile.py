from tkinter import Frame
import closed_card


class CardPile(Frame):

    def __init__(self, master, settings):
        super().__init__(master)

        self.amount = 0
        self.settings = settings

    def set_amount(self, amount):
        """
        Set the deck card amount
        :param amount: str to int
        :return:
        """
        self.amount = int(amount)
        self.draw()

    def draw(self):
        """
        Draws the deck on table if there are any cards left
        """
        if self.amount == 0:
            for child in self.winfo_children():
                del child
                return
        else:
            card_amount = self.amount
            if self.amount > 4:
                card_amount = 4
            last_card_amount = 0
            for widget in self.winfo_children():
                if type(widget) == closed_card.Card:
                    last_card_amount += 1
            if card_amount != last_card_amount:
                for card in self.winfo_children():
                    del card
                offset = int(self.settings["deck_offset"])
                for i in range(card_amount):
                    card = closed_card.Card(self)
                    card.place(x=i*offset, y=i*offset)
                    card.lift()
