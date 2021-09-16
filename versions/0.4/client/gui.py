from card import OpenedCard, calculate_size
from tkinter import *
from utilities import *
import cardpile
import pilerow


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

        # Frames
        self.sidebar_frame = Frame(self.root)
        self.main_frame = Frame(self.root)
        row_height = int(self.settings["row_height"])
        self.card_frame = pilerow.Row(self.main_frame, row_height)
        self.opponents_frame = pilerow.Row(self.main_frame, row_height)
        self.game_frame = pilerow.Row(self.main_frame, row_height)

        # Game variables
        self.cards = []
        self.opponents = {}

        self.draw_window()

        # Deck
        self.deck = cardpile.InteractPile(self.game_frame, self.settings, self.settings["deck_name"])
        self.place_deck()
        self.deck.draw()
        self.deck.bind("<Button-1>", lambda event: self.show_error(":D"))

        # Gamepile
        self.gamepile = cardpile.InteractPile(self.game_frame, self.settings, self.settings["game_name"])
        self.place_gamepile()
        self.gamepile.draw()

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

    def show_error(self, message):
        """
        Shows an error message on screen
        :param message: str
        """
        infolabel = Label(self.root, text=message, font=("Courier", 44))
        infolabel.pack()

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
        green = self.settings["green"]
        sidebar_width = int(self.settings["sidebar_width"])

        # Main frame
        self.main_frame.place(x=0, y=0,
                              width=self.root.winfo_width()-sidebar_width,
                              height=self.root.winfo_height())
        self.main_frame.config(bg=green)

        # Sidebar frame
        self.sidebar_frame.place(x=self.root.winfo_width()-sidebar_width,
                                 y=0,
                                 width=sidebar_width,
                                 height=self.root.winfo_height())
        self.sidebar_frame.config(bg=self.settings["grey"])
        self.root.update()
        self.place_card_frame()
        self.place_game_frame()
        self.place_opponents_frame()
        self.game_frame.update()

    def place_card_frame(self):
        """
        PLaces card frame on table
        """

        height = int(self.settings["row_height"])
        self.card_frame.place_row(x=0, y=self.main_frame.winfo_height() - height)
        self.card_frame.config(bg=self.settings["green"])

    def place_game_frame(self):

        game_frame_pady = int(self.settings["game_frame_pady"])
        self.game_frame.place_row(x=0, y=game_frame_pady)
        self.game_frame.config(bg=self.settings["green"])

    def place_opponents_frame(self):
        """
        Places opponent frame on table
        """
        self.opponents_frame.place_row(x=0, y=0)
        self.opponents_frame.config(bg=self.settings["green"])

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

    def add_cards(self, data):
        """
        Add new cards to hand
        :param data: list of str
        """
        for card in data:
            self.add_card(card)

        self.draw_cards()

    def add_card(self, card_str):
        """
        Adds a new card to hand
        :param card_str: str, XY where X is rank and Y is suit
        """
        rank = card_str[0]
        if rank == "1":
            rank = "10"
            suit = card_str[2]
        else:
            suit = card_str[1]

        card = OpenedCard(self.card_frame, rank, suit)
        card.config(command=lambda: self.client.send(str(card)))
        self.cards.append(card)

    def draw_cards(self):
        """
        Draws player's cards in hand
        """

        frame_width = self.card_frame.winfo_width()       # Width of frame
        card_width = calculate_size()[0]    # Width of a card
        card_pad = int(self.settings["card_padx"])
        first_coordinate = (frame_width - card_pad * (len(self.cards) - 1)
                            - card_width) / 2

        for n, card in enumerate(self.cards):
            coordinate = first_coordinate + (n * card_pad)
            card.place(x=coordinate, y=int(self.settings["card_pady"]))
            card.lift()

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
        w, _ = calculate_size()

        width = self.opponents_frame.winfo_width()
        pile_width = calculate_size()[0] + 3 * int(self.settings["cardpile_offset"])

        first_coordinate = (width - offset * (len(self.opponents) - 1) - pile_width) / 2

        for index, opponent in enumerate(self.opponents):
            x = first_coordinate + (index * (offset+pile_width))

            self.opponents[opponent].place_pile(x=x)