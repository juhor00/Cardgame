try:
    from .hand import Hand
    from .claimgrid import ClaimGrid
    from .turnlist import TurnList
    from .cardpile import *
    from .opponents import Opponents
    from .claim import ClaimText
except ImportError:
    from hand import Hand
    from claimgrid import ClaimGrid
    from turnlist import TurnList
    from cardpile import *
    from opponents import Opponents
    from claim import ClaimText


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
        self.deck = InteractPile(self, "Deck")
        self.gamedeck = InteractPile(self, "Game")
        self.claimgrid = ClaimGrid(self)
        self.opponents = Opponents(self)
        self.claim = Claim(self)

        self.place_widgets()
        self.lower_play_cards()

    def place_widgets(self):
        """
        Places widgets on frame
        """
        self.deck.place(x=80, y=220)
        self.gamedeck.place(x=500, y=220)
        self.hand.place(x=270, y=480)
        self.claimgrid.place(x=870, y=530)
        self.claim.place(x=680, y=220)
        self.opponents.place(x=0, y=4)
        self.play_cards.place(x=270, y=230)

    def lift_play_cards(self):
        """
        Places play cards on top of game deck
        """
        self.gamedeck.lower()
        self.play_cards.lift()
        self.claim.lift()

    def lower_play_cards(self):
        """
        Remove play cards and show game deck
        """
        self.play_cards.lower()
        self.gamedeck.lift()
        self.claim.lift()

    def modify_opponent(self, uid, name, amount, turn, played, suspected):
        """
        Modify opponent info
        :param uid: int
        :param name: str
        :param amount: int
        :param turn: bool
        :param played: bool
        :param suspected: bool
        """
        self.opponents.set_name(uid, name)
        self.opponents.set_amount(uid, amount)
        self.opponents.set_played(uid, played)
        self.opponents.set_turn(uid, turn)
        self.opponents.set_suspected(uid, suspected)

    def add_opponent(self, uid, name, amount, turn):
        """
        Add opponent to Opponents and Turn
        :param uid: int
        :param name: str
        :param amount: int
        :param turn: bool
        """
        self.opponents.add(uid, name, amount)
        self.opponents.set_turn(uid, turn)
