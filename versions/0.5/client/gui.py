from card import calculate_size
from tkinter import *
from utilities import *
import cardpile
import pilerow
import hand
import lobby


class Gui:

    def __init__(self):

        # Comms
        self.client = None
        
        # Settings
        yml = Parser("settings/settings.yml")
        self.settings = yml.read()

        # Window self.settings
        self.root = Tk()
        screen_width = self.settings["screen_width"]
        screen_height = self.settings["screen_height"]
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.minsize(screen_width, screen_height)
        self.root.config(bg="black")
        self.is_fullscreen = False
        self.root.bind("f", self.set_fullscreen)

        self.lobby = lobby.Lobby(self.root, screen_width, screen_height)

        # Frames
        self.sidebar_frame = Frame(self.root, bg=self.settings["grey"])
        self.main_frame = Frame(self.root, bg=self.settings["green"])
        row_height = int(self.settings["row_height"])
        self.card_frame = pilerow.Row(self.main_frame, row_height)
        self.opponents_frame = pilerow.Row(self.main_frame, row_height)
        self.game_frame = pilerow.Row(self.main_frame, row_height)

        self.card_frame.config(bg=self.settings["green"])
        self.opponents_frame.config(bg=self.settings["green"])
        self.game_frame.config(bg=self.settings["green"])
        self.draw_window()

        # Game variables
        self.opponents = {}

        # Hand
        self.hand = hand.Hand(self.card_frame, self.settings)
        bind_event_data(self.hand, "<<Card-clicked>>", self.on_click)

        # Deck
        self.deck = cardpile.InteractPile(self.game_frame, self.settings, self.settings["deck_name"])
        self.place_deck()
        self.deck.draw()
        self.deck.bind("<<Card-clicked>>", lambda event: print("Jee"))

        # Gamepile
        self.gamepile = cardpile.InteractPile(self.game_frame, self.settings, self.settings["game_name"])
        self.place_gamepile()
        self.gamepile.draw()
        self.gamepile.bind("<<Card-clicked>>", lambda event: None)

    def __del__(self):
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

    def set_fullscreen(self, event):
        """
        Sets between fullscreen and windowed
        """
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", False)
            self.is_fullscreen = False
        else:
            self.root.attributes("-fullscreen", True)
            self.is_fullscreen = True

    def show_error(self, message):
        """
        Shows an error message on screen
        :param message: str
        """
        infolabel = Label(self.root, text=message, font=("Courier", 44))
        infolabel.pack()

    @staticmethod
    def on_click(event):
        """
        Action when a hand card is clicked
        :param event: tk event with card info as data
        """
        card = event.data["content"]
        print(card)

    def start(self):
        """
        Strart GUI
        """
        self.root.mainloop()
        del self

    def draw_window(self):
        """
        Draws the background
        """
        self.root.update()
        sidebar_width = int(self.settings["sidebar_width"])

        # Main frame
        self.main_frame.place(x=0, y=0,
                              width=self.root.winfo_width()-sidebar_width,
                              height=self.root.winfo_height())
        # Sidebar frame
        self.sidebar_frame.place(x=self.root.winfo_width()-sidebar_width,
                                 y=0,
                                 width=sidebar_width,
                                 height=self.root.winfo_height())
        self.root.update()
        self.place_frames()
        self.game_frame.update()

    def place_frames(self):
        """
        Places all frames on screen
        """
        height = int(self.settings["row_height"])
        self.card_frame.place_row(x=0, y=self.main_frame.winfo_height() - height)

        game_frame_pady = int(self.settings["game_frame_pady"])
        self.game_frame.place_row(x=0, y=game_frame_pady)
        self.opponents_frame.place_row(x=0, y=0)

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

    def update_opponent(self, data):
        """
        Updates opponents
        :param data: dict
        """
        name = data["name"]
        amount = int(data["amount"])
        won = bool(data["won"])
        lost = bool(data["lost"])

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
