from tkinter import *

try:
    from .mainwindow.mainwindow import MainWindow
    from .lobby.lobby import Lobby
except ImportError:
    from mainwindow.mainwindow import MainWindow
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

    def __init__(self):
        super().__init__()

        self.size = (1280, 720)
        self.minsize(1280, 720)
        self.gamewindow = MainWindow(self, self.size[0], self.size[1])
        self.lobby = Lobby(self, self.size[0], self.size[1])
        self.render_lobby()
        self.in_turn = False
        self.is_fullscreen = False
        self.set_binds()

    def set_turn(self, state):
        self.in_turn = state

    def render_gamewindow(self, *args):
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


if __name__ == "__main__":
    gui = Gui()
    gui.lobby.bind("<<Ready>>", gui.render_gamewindow)
    #gui.gamewindow.test_values()
    gui.mainloop()
