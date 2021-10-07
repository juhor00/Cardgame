from tkinter import *
try:
    from .hand import Hand
    from .claimgrid import ClaimGrid
    from .turnlist import TurnList
    from .cardpile import CardPile, InteractPile
    from .opponents import Opponents
    from .claim import Claim
except ImportError:
    from hand import Hand
    from claimgrid import ClaimGrid
    from turnlist import TurnList
    from cardpile import CardPile, InteractPile
    from opponents import Opponents
    from claim import Claim


class GameWindow(Frame):
    """
    Game window
    """
    def __init__(self, parent, width, height):
        """
        Intialize window
        :param parent: parent widget
        :param width: int
        :param height: int
        """
        super().__init__(parent, width=width, height=height, bg="#35654d")
        self.parent = parent

        self.hand = Hand(self)
        self.play_cards = Hand(self)
        self.turn = TurnList(self)
        self.deck = InteractPile(self, "Deck")
        self.gamedeck = InteractPile(self, "Game")
        self.claimgrid = ClaimGrid(self)
        self.opponents = Opponents(self)
        self.claim = Claim(self)

        self.place_widgets()
        self.remove_play_cards()

    def place_widgets(self):
        """
        Places widgets on frame
        """
        self.deck.place(x=80, y=220)
        self.gamedeck.place(x=500, y=220)
        self.hand.place(x=270, y=480)
        self.claimgrid.place(x=870, y=530)
        self.claim.place(x=880, y=340)
        self.turn.place(x=1060, y=240)
        self.opponents.place(x=0, y=4)
        self.play_cards.place(x=270, y=230)

    def place_play_cards(self):
        """
        Places play cards on top of game deck
        """
        self.gamedeck.lower()
        self.play_cards.lift()

    def remove_play_cards(self):
        """
        Remove play cards and show game deck
        """
        self.play_cards.lower()
        self.gamedeck.lift()


if __name__ == "__main__":
    root = Tk()
    mainwindow = GameWindow(root, 1280, 720)
    mainwindow.test_values()
    mainwindow.pack()
    root.mainloop()