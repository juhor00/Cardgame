from tkinter import Frame, Label
import closed_card


class CardPile(Frame):

    def __init__(self, master, settings, name=""):
        super().__init__(master)

        self.amount = 0
        self.settings = settings
        self.config(bg=self.settings["green"])
        offset = int(self.settings["cardpile_offset"])
        w, h = closed_card.calculate_size()
        self.size = (w+3*offset, h+3*offset)

        self.amount_label = Label(master, text=f"[{self.amount}]", font=("", 12), fg="white", bg=self.settings["green"])

        self.name = name
        self.name_label = Label(master, text=name, font=("", 12), fg="white", bg=self.settings["green"])

    def set_amount(self, amount):
        """
        Set the deck card amount
        :param amount: str to int
        :return:
        """
        self.amount = int(amount)
        self.amount_label.config(text=f"[{self.amount}]")
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
                offset = int(self.settings["cardpile_offset"])
                for i in range(card_amount):
                    card = closed_card.Card(self)
                    card.place(x=i*offset, y=i*offset)
                    card.lift()



    def place_pile(self, x, y):
        """
        Places card pile on coordinates
        :param x: int
        :param y: int
        """
        self.place(x=x, y=y, width=self.size[0], height=self.size[1])

        self.place_name(x, y)

    def place_amount(self, x, y):
        padx = int(self.settings["cardpile_amount_padx"])
        pady = int(self.settings["cardpile_amount_pady"])

        self.amount_label.place(x=x+padx, y=y+pady)
        self.amount_label.lift()

    def place_name(self, x, y):
        """
        Places pile's name Label
        """
        padx = int(self.settings["cardpile_name_padx"])
        pady = int(self.settings["cardpile_name_pady"])

        self.name_label.place(x=x + padx, y=y + self.size[1] + pady)
        self.place_amount(x + padx, y + self.size[1] + pady)
