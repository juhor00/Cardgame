from tkinter import *

try:
    from .gamewindow.gamewindow import GameWindow
    from .lobby.lobby import Lobby
except ImportError:
    from gamewindow.gamewindow import GameWindow
    from lobby.lobby import Lobby


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args):
        e = lambda: None
        e.data = eval(args[0])
        e.widget = widget
        return e,

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format('+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)


class Gui(Tk):
    """
    Graphical interface of client
    """

    def __init__(self, status):
        """
        Initialize Gui
        :param status:
        """
        super().__init__()

        self.status = status
        self.size = (1280, 720)
        self.minsize(1280, 720)
        self.gamewindow = GameWindow(self, self.size[0], self.size[1])
        self.lobby = Lobby(self, self.size[0], self.size[1])
        self.render_lobby()
        self.is_fullscreen = False
        self.set_binds()

        self.update_types = {
            "in_lobby": lambda value: self.render_lobby() if value else self.render_gamewindow(),
            "opponents_modify": lambda opponents: self.modify_opponents(opponents),
            "opponents_add": lambda opponents: self.add_opponents(opponents),
            "opponents_remove": lambda opponents: self.remove_opponents(opponents),
            "deck_amount": lambda value: self.gamewindow.deck.set_amount(value),
            "gamedeck_amount": lambda amount: self.gamewindow.gamedeck.set_amount(amount),
            "claim": lambda claim: self.claim(claim),
            "display_add": lambda cards: self.add_display(cards),
            "display_remove": lambda cards: self.remove_display(cards),
            "hand_cards_add": lambda cards: self.gamewindow.hand.add_cards(cards),
            "hand_cards_remove": lambda cards: self.gamewindow.hand.remove_cards(cards),
            "play_cards_add": lambda cards: self.gamewindow.play_cards.add_cards(cards),
            "play_cards_remove": lambda cards: self.remove_play_cards(cards),
            "allowed_claims": lambda buttons: self.gamewindow.claimgrid.enable_buttons(buttons),
            "denied_claims": lambda buttons: self.gamewindow.claimgrid.disable_buttons(buttons),
            "turn": lambda turn: self.gamewindow.turn.show() if turn else self.gamewindow.turn.hide(),
            "duration": lambda duration: self.gamewindow.claim.start_flicker(duration),
            "discarded": lambda discarded: self.gamewindow.eventlist.discard() if discarded else None,
            "suspect_event": lambda s: self.gamewindow.eventlist.suspected(s[0], s[1]) if s[0] is not None else None
        }

    def update_status(self, status):
        """
        Update Gui status
        :param status: Status
        """
        changes = status.compare(self.status)
        print("GUI changes:", changes)
        self.status = status
        self.apply_changes(changes)

    def apply_changes(self, changes):

        attributes = changes.get_attributes()
        for attribute in attributes:
            value = attributes[attribute]
            self.update_types[attribute](value)

    def render_gamewindow(self):
        """
        Renders gamewindow and hide lobby
        """
        self.lobby.pack_forget()
        self.gamewindow.pack()

    def render_lobby(self):
        self.gamewindow.pack_forget()
        self.lobby.pack()

    def get_name(self):
        """
        Return user nickname
        :return: str
        """
        return self.lobby.get_name()

    def set_fullscreen(self, _):
        """
        Sets between fullscreen and windowed
        """
        if self.is_fullscreen:
            self.attributes("-fullscreen", False)
            self.is_fullscreen = False
        else:
            self.attributes("-fullscreen", True)
            self.is_fullscreen = True

    def set_binds(self):
        """
        Set GUI action binds
        """
        self.bind("<F11>", self.set_fullscreen)
        self.bind("<Escape>", lambda event: self.destroy())

        bind_event_data(self.gamewindow.hand, "<<Card-clicked>>", self.on_hand_click)
        bind_event_data(self.gamewindow.play_cards, "<<Card-clicked>>", self.on_play_click)

    def on_hand_click(self, event):
        """
        Action when hand cards clicked
        :param event: tkinter event
        """
        if self.status.is_displaying():
            return

        if self.status.is_in_turn():
            if len(self.gamewindow.play_cards.get_cards()) >= 4:
                return
            card = event.data["content"]
            self.gamewindow.hand.remove_cards([card])
            self.gamewindow.play_cards.add_cards([card])
            self.update_card_status()

            if len(self.gamewindow.play_cards.get_cards()) > 1:
                # Disable 2, 10 and Ace because they can be only played 1 at a time
                denied_new = {"2": 9, "10": 9, "14": 9}

                denied = self.status.get_denied_claims()
                denied_new.update(denied)

                self.status.set_denied_claims(denied_new)
                self.gamewindow.claimgrid.disable_buttons(denied_new, temp=True)

        # Show play cards
        if not self.gamewindow.play_cards.is_empty():
            self.gamewindow.lift_play_cards()

    def on_play_click(self, event):
        """
        Action when play cards clicked
        :param event: tkinter event
        """
        if self.status.is_displaying():
            return

        if self.status.is_in_turn():
            card = event.data["content"]
            self.gamewindow.play_cards.remove_cards([card])
            self.gamewindow.hand.add_cards([card])
            self.update_card_status()

            if len(self.gamewindow.play_cards.get_cards()) <= 1:
                # Enable 2, 10 and Ace because they can be played
                enable = {2, 10, 14}
                allowed = set(self.status.get_allowed_claims())
                denied = set(self.status.get_denied_claims())
                allowed = allowed.union(enable)-denied

                self.status.set_allowed_claims(list(allowed))
                self.gamewindow.claimgrid.enable_buttons(list(enable), temp=True)

        # Show deck
        if self.gamewindow.play_cards.is_empty():
            self.gamewindow.lower_play_cards()

    def modify_opponents(self, opponents):

        if self.status.is_in_lobby():
            for opponent in opponents:
                self.lobby.modify_opponent(opponent.get_uid(), opponent.get_name(), opponent.is_ready())
        else:
            for opponent in opponents:
                uid = opponent.get_uid()
                amount = opponent.get_card_amount()
                turn = opponent.is_in_turn()
                name = opponent.get_name()
                played = opponent.has_played()
                suspected = opponent.has_suspected()

                self.gamewindow.modify_opponent(uid, name, amount, turn, played, suspected)

    def add_opponents(self, opponents):

        for opponent in opponents:
            uid = opponent.get_uid()
            name = opponent.get_name()
            ready = opponent.is_ready()
            amount = opponent.get_card_amount()
            turn = opponent.is_in_turn()
            self.lobby.add_opponent(uid, name, ready)

            if uid == self.status.uid:
                name = "You"
            self.gamewindow.add_opponent(uid, name, amount, turn)

    def remove_opponents(self, opponents):
        """
        Ignore opponents to remove and refresh all with current status info
        :param opponents:
        """
        if self.status.is_in_lobby():
            self.lobby.remove_all_and_add_opponents(self.status.get_opponents())

    def update_card_status(self):
        hand_cards = self.gamewindow.hand.get_cards()
        play_cards = self.gamewindow.play_cards.get_cards()

        self.status.set_play_cards(play_cards)
        self.status.set_hand_cards(hand_cards)

    def add_display(self, cards):
        self.gamewindow.claim.stop_flicker()
        self.gamewindow.play_cards.add_cards(cards)
        self.gamewindow.lift_play_cards()

    def remove_display(self, cards):
        self.gamewindow.play_cards.remove_cards(cards)
        self.gamewindow.lower_play_cards()

    def remove_play_cards(self, cards):
        self.gamewindow.play_cards.remove_cards(cards)
        self.gamewindow.claim.stop_flicker()

    def claim(self, claim):
        """
        Set new claim.
        Add play event (normal or deck)
        :param claim: claim changes: int, int, int, str, bool
        """
        amount, rank, claim_id, name, deck = claim
        self.gamewindow.claim.new(amount, rank)
        name = claim[3]
        deck = claim[4]

        if amount:
            if not deck:
                self.gamewindow.eventlist.played_cards(name)
            else:
                self.gamewindow.eventlist.played_deck(name)