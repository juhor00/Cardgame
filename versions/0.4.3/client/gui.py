from card import calculate_size
from tkinter import *
from utilities import *
import cardpile
import pilerow
import hand
import claimgrid
import lobby


def bind_event_data(widget, sequence, func, add=None):
    def _substitute(*args):
        e = lambda: None
        e.data = eval(args[0])
        e.widget = widget
        return e,

    funcid = widget._register(func, _substitute, needcleanup=1)
    cmd = '{0}if {{"[{1} %d]" == "break"}} break\n'.format('+' if add else '', funcid)
    widget.tk.call('bind', widget._w, sequence, cmd)


class Gui:

    def __init__(self):

        # Comms
        self.client = None
        
        # Settings
        yml = Parser("settings/settings.yml")
        self.settings = yml.read()
        screen_width = self.settings["screen_width"]
        screen_height = self.settings["screen_height"]

        # Window
        self.root = Tk()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.minsize(screen_width, screen_height)
        self.root.config(bg="black")
        self.is_fullscreen = False
        self.root.bind("f", self.set_fullscreen)
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        # Lobby
        self.lobby = lobby.Lobby(self.root, width=screen_width, height=screen_height)
        self.lobby.bind("<<Ready>>", self.on_lobby_ready)
        self.lobby.bind("<<Cancel>>", self.on_lobby_cancel)

        # Frames
        sidebar_width = int(self.settings["sidebar_width"])
        self.main_frame = Frame(self.root, bg=self.settings["green"])
        self.main_frame.config(width=self.root.winfo_width() - sidebar_width, height=self.root.winfo_height())
        self.sidebar_frame = Frame(self.root, bg=self.settings["grey"])
        self.sidebar_frame.config(width=sidebar_width, height=self.root.winfo_height())
        self.root.update()

        row_height = int(self.settings["row_height"])
        self.card_frame = pilerow.Row(self.main_frame, row_height)
        self.opponents_frame = pilerow.Row(self.main_frame, row_height)
        self.game_frame = pilerow.Row(self.main_frame, row_height)

        self.card_frame.config(bg=self.settings["green"])
        self.opponents_frame.config(bg=self.settings["green"])
        self.game_frame.config(bg=self.settings["green"])
        self.root.update()

        # Game variables
        self.opponents = {}

        # Hand
        self.hand = hand.Hand(self.card_frame, self.settings)
        bind_event_data(self.hand, "<<Card-clicked>>", self.on_hand_click)

        # Deck
        self.deck = cardpile.InteractPile(self.game_frame, self.settings, self.settings["deck_name"])
        self.deck.bind("<<Card-clicked>>", self.on_deck)

        # Gamepile
        self.gamepile = cardpile.InteractPile(self.game_frame, self.settings, self.settings["game_name"])
        self.gamepile.bind("<<Card-clicked>>", self.on_suspect)

        # Played cards
        self.play_cards = hand.Hand(self.game_frame, self.settings)
        bind_event_data(self.play_cards, "<<Card-clicked>>", self.on_play_click)

        # Claim buttons
        self.claimgrid = claimgrid.ClaimGrid(self.card_frame, self.settings)
        bind_event_data(self.claimgrid, "<<Button-clicked>>", self.on_claim)
        self.place_claimgrid()

        self.draw_lobby()
        self.draw_window()

    def __del__(self, event=None):
        """
        Disconnect from server
        """
        if self.client:
            self.client.send_general("disconnect")

    def set_client(self, client):
        """
        Sets the client for communications
        :param client: Client instance
        """
        self.client = client
        # Receive thread
        new_thread(self.client.receive)

    def set_fullscreen(self, _):
        """
        Sets between fullscreen and windowed
        """
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", False)
            self.is_fullscreen = False
        else:
            self.root.attributes("-fullscreen", True)
            self.is_fullscreen = True

    def show_message(self, text, permanent=False, delay=4):
        """
        Shows a temporary message on screen
        :param text: str
        :param permanent: bool
        :param delay: int
        """

        label = Label(self.root, text=text, font=("Courier", 44))
        label.pack()
        if not permanent:
            label.after(delay*1000, label.destroy)

    def on_hand_click(self, event):
        """
        Action when a hand card is clicked
        :param event: tk event with card info as data
        """
        card = event.data["content"]
        self.hand.remove_cards([card])
        self.play_cards.add_cards([card])

    def on_play_click(self, event):
        """
        Action when a played card is clicked
        :param event: tk event with card info as data
        """
        card = event.data["content"]
        self.play_cards.remove_cards([card])
        self.hand.add_cards([card])

    def on_claim(self, event):
        """
        Action when player clicked a claim button
        :param event: tk event with button info as data
        """
        button = event.data["content"]
        print(button)

    def on_deck(self, event=None):
        """
        Action when deck is clicked
        :param event: tk event
        """
        print("Deck")

    def on_suspect(self, event=None):
        """
        Action when player clicked the game pile
        :param event: tk event
        """
        print("Epäily")

    def on_lobby_ready(self, event=None):
        """
        Action when Ready is clicked in lobby
        :param event: tk event
        """
        print("Ready")

    def on_lobby_cancel(self, event=None):
        """
        Action when Cancel is clicked in lobby
        :param event: tk event
        """
        print("Cancel")

    def start(self):
        """
        Strart GUI
        """
        self.root.mainloop()
        del self

    def draw_lobby(self):
        """
        Draws the lobby
        """
        for child in self.root.winfo_children():
            child.place_forget()
        self.lobby.place(x=0, y=0)

    def draw_window(self):
        """
        Draws the background
        """
        for child in self.root.winfo_children():
            child.place_forget()
        self.root.update()
        sidebar_width = int(self.settings["sidebar_width"])

        # Main frame
        self.main_frame.place(x=0, y=0)
        # Sidebar frame
        self.sidebar_frame.place(x=self.root.winfo_width()-sidebar_width, y=0)
        self.root.update()
        self.place_frames()
        self.game_frame.update()

        self.place_deck()
        self.deck.draw()

        self.place_gamepile()
        self.gamepile.draw()

    def place_frames(self):
        """
        Places all frames on screen
        """
        height = int(self.settings["row_height"])
        self.card_frame.place_row(x=0, y=self.main_frame.winfo_height() - height)

        game_frame_pady = int(self.settings["game_frame_pady"])
        self.game_frame.place_row(x=0, y=game_frame_pady)
        self.opponents_frame.place_row(x=0, y=0)
        self.card_frame.update()

    def place_deck(self):
        """
        Places deck on table
        """
        deck_padx = int(self.settings["deck_padx"])
        self.deck.place_pile(x=deck_padx)

    def place_gamepile(self):
        """
        Places gamepile on table
        """
        padx = int(self.settings["gamepile_padx"])
        self.gamepile.place_pile(x=padx)

    def place_claimgrid(self):
        """
        Place claimgrid on table
        """
        padx = int(self.settings["claimgrid_padx"])
        pady = int(self.settings["claimgrid_pady"])
        self.claimgrid.place(x=padx, y=pady)

    def update_opponent(self, data):
        """
        Updates opponents
        :param data: dict
        """
        name = data["name"]
        amount = int(data["amount"])

        if name not in self.opponents:
            opponent = cardpile.CardPile(self.opponents_frame, self.settings, name)
            self.opponents[name] = opponent
        else:
            opponent = self.opponents[name]

        opponent.set_amount(amount)
        self.place_opponents()

    def place_opponents(self):
        """
        Places opponents on the frame
        """
        offset = int(self.settings["opponent_offset"])

        width = self.opponents_frame.winfo_width()
        pile_width = calculate_size()[0] + 3 * int(self.settings["cardpile_offset"])

        first_coordinate = (width - (offset+pile_width) * (len(self.opponents) - 1) - pile_width) / 2

        for index, opponent in enumerate(self.opponents):
            x = first_coordinate + (index * (offset+pile_width))

            self.opponents[opponent].place_pile(x=x)


class Message:

    def __init__(self, master, text, permanent=False):
        self.label = Label(master, text=text, font=("Courier", 44))

        if permanent:
            self.permanent()
        else:
            self.temporary()

    def permanent(self):
        """
        Shows a permanent message
        """
        self.label.pack()

    def temporary(self):
        """
        Shows a temporary message
        :return:
        """
        self.label.pack()
        self.label.after(1000, self.label.destroy)
