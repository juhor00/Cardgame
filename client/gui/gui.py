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
            "denid_claims": lambda buttons: self.gamewindow.claimgrid.disable_buttons(buttons),
        }

    def update_status(self, status):
        """
        Update Gui status
        :param status: Status
        """
        changes = status.compare(self.status)
        self.status = status
        print("Status:", vars(status))
        print("Changes:", vars(changes))
        self.apply_changes(changes)

    def apply_changes(self, changes):

        attributes = changes.get_attributes()
        for attribute in attributes:
            value = attributes[attribute]
            print(attribute, value)
            self.update_types[attribute](value)

    def set_turn(self, state):
        self.in_turn = state

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
        self.bind("f", self.set_fullscreen)
        self.bind("<Escape>", lambda event: self.destroy())

        bind_event_data(self.gamewindow.hand, "<<Card-clicked>>", self.on_hand_click)
        bind_event_data(self.gamewindow.play_cards, "<<Card-clicked>>", self.on_play_click)

    def on_hand_click(self, event):
        if self.in_turn:
            card = event.data["content"]
            self.gamewindow.hand.remove_card(card)
            self.gamewindow.play_cards.add_card(card)

    def on_play_click(self, event):
        if self.in_turn:
            card = event.data["content"]
            self.gamewindow.play_cards.remove_card(card)
            self.gamewindow.hand.add_card(card)

    def modify_opponents(self, opponents):

        if self.status.is_in_lobby():
            for opponent in opponents:
                self.lobby.modify_opponent(opponent.get_uid(), opponent.get_name(), opponent.is_ready())

    def add_opponents(self, opponents):

        if self.status.is_in_lobby():
            for opponent in opponents:
                print("Add:", vars(opponent))
                self.lobby.add_opponent(opponent.get_uid(), opponent.get_name(), opponent.is_ready())

    def remove_opponents(self, _):
        """
        Ignore opponents to remove and refresh all with current status info
        :param _: opponents, ignored
        """
        self.lobby.remove_all_and_add_opponents(self.status.get_opponents())

    def add_display(self, cards):
        pass

    def remove_display(self, cards):
        pass
