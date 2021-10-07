from tkinter import *

try:
    from .mainwindow.gamewindow import GameWindow
    from .lobby.lobby import Lobby
except ImportError:
    from mainwindow.gamewindow import GameWindow
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
        self.gamewindow.turn.add(self.status.get_uid(), "You", self.status.get_turn())

        self.update_types = {
            "in_lobby": lambda value: self.render_lobby() if value else self.render_gamewindow(),
            "opponents_modify": lambda opponents: self.modify_opponents(opponents),
            "opponents_add": lambda opponents: self.add_opponents(opponents),
            "opponents_remove": lambda opponents: self.remove_opponents(opponents),
            "deck_amount": lambda value: self.gamewindow.deck.set_amount(value),
            "gamedeck_amount": lambda value: self.gamewindow.gamedeck.set_amount(value),
            "claim": lambda claim: self.gamewindow.claim.new(claim[0], claim[1]),
            "display_add": lambda cards: self.add_display(cards),
            "display_remove": lambda cards: self.remove_display(cards),
            "hand_cards_add": lambda cards: self.gamewindow.hand.add_cards(cards),
            "hand_cards_remove": lambda cards: self.gamewindow.hand.remove_cards(cards),
            "play_cards_add": lambda cards: self.gamewindow.play_cards.add_cards(cards),
            "play_cards_remove": lambda cards: self.gamewindow.play_cards.remove_cards(cards),
            "allowed_claims": lambda buttons: self.gamewindow.claimgrid.enable_buttons(buttons),
            "denied_claims": lambda buttons: self.gamewindow.claimgrid.disable_buttons(buttons),
            "turn": lambda value: None
        }

    def update_status(self, status):
        """
        Update Gui status
        :param status: Status
        """
        changes = status.compare(self.status)
        self.status = status
        print(vars(changes))
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
        if self.status.get_turn():
            card = event.data["content"]
            self.gamewindow.hand.remove_cards([card])
            self.gamewindow.play_cards.add_cards([card])
            self.update_card_status()

    def on_play_click(self, event):
        if self.status.get_turn():
            card = event.data["content"]
            self.gamewindow.play_cards.remove_cards([card])
            self.gamewindow.hand.add_cards([card])
            self.update_card_status()

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

                self.gamewindow.modify_opponent(uid, turn, amount, name)

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

    def remove_opponents(self, _):
        """
        Ignore opponents to remove and refresh all with current status info
        :param _: opponents, ignored
        """
        if self.status.is_in_lobby():
            self.lobby.remove_all_and_add_opponents(self.status.get_opponents())

    def add_display(self, cards):
        pass

    def remove_display(self, cards):
        pass

    def update_card_status(self):
        hand_cards = self.gamewindow.hand.get_cards()
        play_cards = self.gamewindow.play_cards.get_cards()

        self.status.set_hand_cards(hand_cards)
        self.status.set_play_cards(play_cards)
