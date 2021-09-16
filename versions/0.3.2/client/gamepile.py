import cardpile
import closed_card
from card import calculate_size


class GamePile(cardpile.CardPile):

    def __init__(self, master, settings, name):
        super().__init__(master, settings, name)

        self.elevated = False
        self.elevated_y = None
        self.elevated_x = None
        self.normal_y = None
        self.normal_x = None
        self.top = None

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Motion>", self.on_enter)

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

        if event.x <= w + elevate_x:
            return

        top = self.get_top_card()
        if top is None:
            return

        # Set coordinates
        if not self.elevated_set():
            y = top.winfo_y()
            x = top.winfo_x()

            self.elevated_y = y - elevate_y
            self.elevated_x = x + elevate_x
            self.normal_y = y
            self.normal_x = x

        self.elevated = True
        top.place(y=self.elevated_y, x=self.elevated_x)

    def on_leave(self, event):
        """
        Lowers the card when not hovered over anymore
        """
        if not self.elevated:
            return

        top = self.get_top_card()
        if top is None:
            return

        self.elevated = False
        top.place(y=self.normal_y, x=self.normal_x)

    def elevated_set(self):
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

    def get_top_card(self):
        """
        Returns the topmost card
        :return: closed_card.Card
        """
        # Top card
        cards = []
        for child in self.winfo_children():
            if type(child) == closed_card.Card:
                cards.append(child)
        if len(cards) == 0:
            return None
        top = cards[-1]
        if top != self.top:
            self.elevated_reset()
        self.top = top
        return cards[-1]
