import card as opened_card
from tkinter import *
from utilities import *
import cardpile


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
        self.card_frame = Frame(self.main_frame)
        self.opponents_frame = Frame(self.main_frame)
        self.game_frame = Frame(self.main_frame)

        # Piles
        self.deck = cardpile.CardPile(self.game_frame, self.settings, "Deck")
        self.gamepile = cardpile.CardPile(self.game_frame, self.settings, "Game")

        # Game variables
        self.cards = []
        self.opponents = {}

        self.draw_window()
        self.place_deck()
        self.place_gamepile()
        self.place_opponents_frame()

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
        card_frame_height = int(self.settings["card_frame_height"])
        game_frame_pady = int(self.settings["game_frame_pady"])

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

        # Card frame
        self.card_frame.place(x=0,
                              y=self.root.winfo_height()-card_frame_height,
                              width=self.root.winfo_width()-sidebar_width,
                              height=card_frame_height)
        self.card_frame.config(bg=green)

        # Game frame
        offset = int(self.settings["cardpile_offset"])
        name_height = int(self.settings["game_frame_name_height"])
        _, h = opened_card.calculate_size()
        self.game_frame.place(x=0, y=game_frame_pady,
                              width=self.main_frame.winfo_width(),
                              height=h+3*offset+name_height)
        self.game_frame.config(bg=self.settings["green"])

    def place_deck(self):
        """
        Places deck on table
        """
        deck_padx = int(self.settings["deck_padx"])
        deck_pady = int(self.settings["deck_pady"])
        self.deck.place_pile(x=deck_padx, y=deck_pady)

    def place_gamepile(self):
        """
        Places gamepile on table
        """
        padx = int(self.settings["gamepile_padx"])
        pady = int(self.settings["gamepile_pady"])
        self.gamepile.place_pile(x=padx, y=pady)

    def place_opponents_frame(self):
        """
        Places opponent frame on table
        """
        height = int(self.settings["opponent_height"])
        sidebar_width = int(self.settings["sidebar_width"])
        w = self.main_frame.winfo_width()
        self.opponents_frame.place(x=0, y=0, width=self.main_frame.winfo_width() - sidebar_width, height=height)
        self.opponents_frame.config(bg=self.settings["green"])

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

        card = opened_card.Card(self.card_frame, rank, suit)
        card.config(command=lambda: self.client.send(str(card)))
        self.cards.append(card)

    def draw_cards(self):
        """
        Draws player's cards in hand
        """

        frame_width = self.card_frame.winfo_width()       # Width of frame
        card_width = opened_card.calculate_size()[0]    # Width of a card
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
        pady = int(self.settings["opponent_pady"])
        offset = int(self.settings["opponent_offset"])
        w, _ = opened_card.calculate_size()

        width = self.opponents_frame.winfo_width()
        pile_width = opened_card.calculate_size()[0] + 3 * int(self.settings["cardpile_offset"])

        first_coordinate = (width - offset * (len(self.opponents) - 1) - pile_width) / 2

        for index, opponent in enumerate(self.opponents):
            x = first_coordinate + (index * (offset+pile_width))

            self.opponents[opponent].place_pile(x=x, y=pady)


