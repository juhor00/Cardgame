from tkinter import Frame, Label
from card import ClosedCard, calculate_size


class CardPile(Frame):

    def __init__(self, master, settings, name=""):
        super().__init__(master)

        self.amount = 0
        self.settings = settings
        self.config(bg=self.settings["green"])
        offset = int(self.settings["cardpile_offset"])
        w, _ = calculate_size()
        h = master.winfo_height()
        self.size = (w+3*offset, h)

        self.amount_label = Label(self, text=f"[{self.amount}]", font=("", 12), fg="white", bg=self.settings["green"])

        self.name = name
        self.name_label = Label(self, text=name, font=("", 12), fg="white", bg=self.settings["green"])

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
                if type(widget) == ClosedCard:
                    last_card_amount += 1
            if card_amount != last_card_amount:
                for card in self.winfo_children():
                    del card
                offset = int(self.settings["cardpile_offset"])
                x = int(self.settings["cardpile_x"])
                y = int(self.settings["cardpile_y"])
                for i in range(card_amount):
                    card = ClosedCard(self)
                    card.place(x=x+i*offset, y=y+i*offset)
                    card.lift()

    def place_pile(self, x):
        """
        Places card pile on coordinates
        :param x: int
        :param y: int
        """
        self.place(x=x, y=0, width=self.size[0], height=self.size[1])

        self.place_name()

    def place_amount(self):
        padx = int(self.settings["cardpile_amount_padx"])
        pady = int(self.settings["cardpile_amount_pady"])

        w, h = self.size
        self.amount_label.place(x=padx, y=h-pady)
        self.amount_label.lift()

    def place_name(self):
        """
        Places pile's name Label
        """
        padx = int(self.settings["cardpile_name_padx"])
        pady = int(self.settings["cardpile_name_pady"])
        w, h = self.size
        self.name_label.place(x=padx, y=h-pady)
        self.place_amount()


class InteractPile(CardPile):

    def __init__(self, master, settings, name):
        super().__init__(master, settings, name)

        self.elevated = False
        self.elevated_y = None
        self.elevated_x = None
        self.normal_y = None
        self.normal_x = None
        self.top = None

        # Add elevate movement to size
        elevate_x = int(self.settings["gamepile_hover_x"])
        elevate_y = int(self.settings["gamepile_hover_y"])
        x, y = self.size
        x += elevate_x
        self.size = (x, y)

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
        elevate_y = int(self.settings["gamepile_hover_y"])
        elevate_x = int(self.settings["gamepile_hover_x"])

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
        Returns the topmost card
        :return: closed_card.Card
        """
        # Top card
        cards = []
        for child in self.winfo_children():
            if type(child) == ClosedCard:
                cards.append(child)
        if len(cards) == 0:
            return None
        top = cards[-1]
        if top != self.top:
            self.elevated_reset()
        top.bind("<Enter>", self.on_enter)
        top.bind("<Leave>", self.on_leave)
        top.bind("<Motion>", self.on_enter)
        top.bind("<Button-1>", self.on_click)
        self.top = top
