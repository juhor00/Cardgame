from tkinter import *

try:
    from .card import ClosedCard, calculate_size
except ImportError:
    from card import ClosedCard, calculate_size


class CardPile(Frame):

    def __init__(self, parent, name=""):

        # Card size
        width, height = calculate_size()
        pad = 8
        info_height = 50
        super().__init__(parent, bg="#35654d", width=width+3*pad, height=height+3*pad+info_height)

        self.amount = 0
        self.name = name

        self.amount_label = Label(self, text=f"[{self.amount}]", font=("", 12), fg="white", bg="#35654d")
        self.name_label = Label(self, text=name, font=("", 12), fg="white", bg="#35654d")

        self.draw()

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
        Draws the pile
        """
        pad = 8
        # Cards
        card_amount = self.amount
        if self.amount > 4:
            card_amount = 4

        for count in range(card_amount):
            card = ClosedCard(self)
            card.place(x=count*pad, y=count*pad)
            card.lift()

        # Amount
        offset = 10
        width, height = calculate_size()
        self.amount_label.place(x=0, y=3 * pad + height + offset)
        self.name_label.place(x=40, y=3*pad + height + offset)

    def get_name(self):
        """
        Return name
        :return: str
        """
        return self.name

    def __str__(self):
        return self.get_name()


class InteractPile(CardPile):
    """
    A card pile that can be interacted with
    """
    def __init__(self, parent, name=""):
        super().__init__(parent, name=name)
        self.update()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        # Add hover
        hover_x = 14
        hover_y = 20
        self.config(width=width + hover_x, height=height+hover_y)

        self.elevated = False
        self.elevated_y = None
        self.elevated_x = None
        self.normal_y = None
        self.normal_x = None
        self.top = None

    def draw(self):

        pad = 8
        hover_y = 20
        # Cards
        card_amount = self.amount
        if self.amount > 4:
            card_amount = 4

        for count in range(card_amount):
            card = ClosedCard(self)
            card.place(x=count * pad, y=count * pad + hover_y)
            card.lift()

        # Amount
        offset = 10
        width, height = calculate_size()
        self.amount_label.place(x=0, y=3 * pad + height + offset + hover_y)
        self.name_label.place(x=40, y=3 * pad + height + offset + hover_y)

    def set_amount(self, amount):
        """
        Update the amount and top card
        :param amount: int
        """
        super().set_amount(amount)
        self.update_top_card()

    def on_enter(self, event):
        """
        Elevate the top card when hovered over
        """
        if self.elevated:
            return

        w, h = calculate_size()
        elevate_y = 20
        elevate_x = 14

        # Allowed coordinates
        if event.y >= h - elevate_y:
            return
        if event.x <= elevate_x:
            return

        if self.top is None:
            return

        # Set coordinates
        if not self.is_elevated_set():
            y = self.top.winfo_y()
            x = self.top.winfo_x()

            self.elevated_y = y - elevate_y
            self.elevated_x = x + elevate_x
            self.normal_y = y
            self.normal_x = x

        self.elevated = True
        self.top.place(y=self.elevated_y, x=self.elevated_x)

    def on_leave(self, event):
        """
        Lowers the card when not hovered over anymore
        """
        if not self.elevated:
            return

        if self.top is None:
            return

        self.elevated = False
        self.top.place(y=self.normal_y, x=self.normal_x)

    def on_click(self, event):
        """
        Generate event if click was allowed
        """
        if self.elevated:
            self.event_generate("<<Card-clicked>>")

    def is_elevated_set(self):
        """
        Return True if elevated place is set
        :return: bool
        """
        return self.elevated_y is not None or self.elevated_x is not None

    def elevated_reset(self):
        self.elevated_y = None
        self.elevated_x = None
        self.normal_x = None
        self.normal_y = None
        self.elevated = False

    def update_top_card(self):
        """
        Updates the top card
        """
        # Top card
        cards = []
        for child in self.winfo_children():
            if type(child) == ClosedCard:
                cards.append(child)
        if len(cards) == 0:
            return
        top = cards[-1]
        if top != self.top:
            if self.top is not None:
                self.top.destroy()
            self.elevated_reset()
        top.bind("<Enter>", self.on_enter)
        top.bind("<Leave>", self.on_leave)
        top.bind("<Motion>", self.on_enter)
        top.bind("<Button-1>", self.on_click)
        self.top = top


if __name__ == "__main__":
    root = Tk()
    cardpile = InteractPile(root, name="Test")
    cardpile.set_amount(10)
    cardpile.pack()
    root.mainloop()
