import json
import socket
import card as card_module
from tkinter import *
from PIL import Image, ImageTk
from utilities import *


def show_error(message):
    infoview = Tk()
    infoview.geometry("640x480")
    infolabel = Label(infoview, text=message, font=("Courier", 44))
    image = Image.open("./assets/sadface.png")
    image = image.resize((200, 150), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    imagelabel = Label(infoview, image=image)
    imagelabel.image = image
    infolabel.pack()
    imagelabel.pack()
    infoview.mainloop()


class Game:

    def __init__(self):

        # Window settings
        self.root = Tk()
        screen_width = settings["screen_width"]
        screen_height = settings["screen_height"]
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Frames
        self.sidebar_frame = Frame(self.root)
        self.main_frame = Frame(self.root)
        self.card_frame = Frame(self.main_frame)
        self.deck_frame = Frame(self.main_frame)
        self.game_frame = Frame(self.main_frame)
        self.opponents_frame = Frame(self.main_frame)

        # Game variables
        self.cards = []

        self.draw_window()

        # Receive thread
        new_thread(self.receive)

        self.root.mainloop()
        del self

    def __del__(self):
        self.send_general("disconnect")

    def draw_window(self):
        """
        Draws the background
        """
        self.root.update()
        green = settings["backgroundcolor"]
        sidebar_width = int(settings["sidebar_width"])
        card_frame_height = int(settings["card_frame_height"])

        self.main_frame.place(x=0, y=0,
                              width=self.root.winfo_width()-sidebar_width,
                              height=self.root.winfo_height())
        self.main_frame.config(bg=green)
        self.sidebar_frame.place(x=self.root.winfo_width()-sidebar_width,
                                 y=0,
                                 width=sidebar_width,
                                 height=self.root.winfo_height())
        self.sidebar_frame.config(bg=settings["sidebar_bg"])

        self.card_frame.place(x=0,
                              y=self.root.winfo_height()-card_frame_height,
                              width=self.root.winfo_width()-sidebar_width,
                              height=card_frame_height)
        self.card_frame.config(bg=settings["card_frame_bg"])

    def draw_cards(self):
        """
        Draws player's cards in hand
        """

        frame_width = self.card_frame.winfo_width()       # Width of frame
        card_width = card_module.calculate_size()[0]    # Width of a card
        card_pad = int(settings["card_pad"])
        first_coordinate = (frame_width - card_pad * (len(self.cards) - 1)
                            - card_width) / 2

        for n, card in enumerate(self.cards):
            coordinate = first_coordinate + (n * card_pad)
            card.place(x=coordinate, y=0)
            card.lift()

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

        new_card = card_module.Card(self.card_frame, rank, suit)
        new_card.config(command=lambda: self.send(str(new_card)))
        self.cards.append(new_card)

    def player_event(self, data):
        """
        Handles player events
        :param data: JSON data
        """
        print("Player: ", data)
        if "add" in data:
            self.add_cards(data["add"])

    def opponent_event(self, data):
        """
        Handles opponent events
        :param data: JSON data
        """
        print("Opponent: ", data)

    def deck_event(self, data):
        """
        Handles deck events
        :param data: JSON data
        """
        print("Deck: ", data)

    def game_event(self, data):
        """
        Handles game events
        :param data: JSON data
        """
        print("Game: ", data)

    def sidebar_event(self, data):
        """
        Handles sidebar events
        :param data: JSON data
        """
        print("Sidebar: ", data)

    def event(self, message):
        """
        Passes data to their handlers
        :param message: received socket message
        """
        data = json.loads(message)

        if "player" in data:
            new_thread(lambda: self.player_event(data["player"]))

        if "opponent" in data:
            new_thread(lambda: self.opponent_event(data["opponent"]))

        if "deck" in data:
            new_thread(lambda: self.deck_event(data["deck"]))

        if "game" in data:
            new_thread(lambda: self.game_event(data["game"]))

        if "sidebar" in data:
            new_thread(lambda: self.sidebar_event(data["sidebar"]))

    def receive(self):
        while True:
            try:
                message = server.recv(1024).decode("UTF-8")
                for json_obj in split_json(message):
                    event_thread = threading.Thread(
                        target=lambda: self.event(json_obj))
                    event_thread.start()
            except socket.error:
                print("An error occurred!")
                server.close()
                break

    def send_general(self, message):
        """
        Send general data
        :param message: str
        """
        data = {"general": message}
        json_obj = json.dumps(data)
        self.send(json_obj)

    @staticmethod
    def send(json_obj):
        """
        Send json object to server
        :param json_obj: JSON data
        """
        byte_obj = bytes(json_obj, encoding="UTF-8")
        server.send(byte_obj)


if __name__ == "__main__":
    yaml = Parser("settings.yml")
    settings = yaml.read()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = settings["host"]                  # Static ip
    host = socket.gethostname()                # Localhost
    port = int(settings["port"])
    try:
        server.connect((host, port))
        new_thread(Game, daemon=False)
    except socket.error:
        show_error("Server offline")
        exit("Server offline")
