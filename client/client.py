import threading
import json
from copy import deepcopy

try:
    from .gui.gui import Gui
    from .network import Network
    from .eventhandler import EventHandler
    from .status import Status
except ImportError:
    from gui.gui import Gui
    from network import Network
    from eventhandler import EventHandler
    from status import Status


def new_thread(target, daemon=True, args=()):
    thread = threading.Thread(target=target, args=args, daemon=daemon)
    thread.start()


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args):
        e = lambda: None
        e.data = eval(args[0])
        e.widget = widget
        return e,

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format('+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)


class Client:
    """
    Cardgame client
    """

    def __init__(self):

        self.network = Network()
        self.send({"general": "connect"})

        self.status = Status(self.network.get_uid())
        self.eventhandler = EventHandler(self)
        self.gui = Gui(deepcopy(self.status))

        new_thread(self.receive)
        self.set_binds()
        self.gui.mainloop()

    def __del__(self):
        """
        Disconnect from the server
        """
        self.network.disconnect()

    def receive(self):
        """
        Get messages from server
        """
        while True:
            try:
                message = json.loads(self.network.get())
                print("CLIENT message:", message)
                self.eventhandler.new(message)
            except json.JSONDecodeError as e:
                print("Stop receiving:", e)
                return

    def send(self, message):
        """
        Send Message object to server
        :param message: dict
        """
        if self.network.is_connected():
            self.network.send(bytes(json.dumps(message), encoding="UTF-8"))

    def set_binds(self):
        """
        Bind network actions
        """
        self.gui.lobby.bind("<<Ready>>", self.on_lobby_ready)
        self.gui.lobby.bind("<<Cancel>>", self.on_lobby_cancel)
        self.gui.gamewindow.gamedeck.bind("<<Card-clicked>>", self.on_suspect)
        self.gui.gamewindow.deck.bind("<<Card-clicked>>", self.on_deck)
        bind_event_data(self.gui.gamewindow.claimgrid, "<<Button-clicked>>", self.on_claim)

    def on_lobby_ready(self, _):
        """
        Action when player is ready in lobby
        :param _: eventhandler
        """
        nickname = self.gui.get_name()
        self.send({"lobby": {"ready": True,
                             "name": nickname}
                   })

    def on_lobby_cancel(self, _):
        """
        Action when player cancels to not ready in lobby
        :param _: eventhandler
        """
        self.send({"lobby": {"ready": False}})

    def on_claim(self, event):
        """
        Action when player claims played cards
        :param event: contains eventhandler data
        """
        rank = int(event.data["content"])
        cards = self.gui.status.get_play_cards()

        self.update_status()
        self.status.set_play_cards([])
        self.update_gui()

        if self.status.is_in_turn():
            print("Send: claim", rank, cards)
            data = {"game": {"played": cards, "claimed": rank}}
            self.send(data)
        else:
            print("Not allowed claim", rank, cards)

    def on_suspect(self, _):
        """
        Action when player suspects
        :param _: eventhandler
        """
        print("Send: suspect")
        self.send({"game": {"suspect": True}})

    def on_deck(self, _):
        """
        Action when deck is clicked
        :param _: eventhandler
        """
        print("Deck")

    def update_gui(self):
        self.gui.update_status(deepcopy(self.status))

    def update_status(self):
        """
        Update gui status based on Gui changes (hand / play cards)
        """
        self.status = deepcopy(self.gui.status)


if __name__ == '__main__':
    client = Client()
