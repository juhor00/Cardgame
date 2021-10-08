from tkinter import *


class TurnList(Frame):

    def __init__(self, master):
        super().__init__(master, bg="#35654d")

        self.players = []

    def add(self, uid, name, turn):
        """
        Add new player
        :param uid: int
        :param name: str
        :param turn: bool
        """

        # Grid players
        max_len = 0
        if len(name) > max_len:
            max_len = len(name)
        player = Player(self, name, uid)
        player.grid(sticky="nsew")
        self.players.append(player)
        print("Turnlist added", name, uid)

        self.update()
        for widget in self.winfo_children():
            if type(widget) == Player:
                widget.config(width=max_len)

        self.set_turn(uid, turn)

    def remove(self, uid):
        """
        Remove player by uid
        :param uid: int
        """
        for player in self.players:
            if player.get_uid() == uid:
                del player
                return

    def set_turn(self, uid, turn):
        """
        Mark player active
        :param uid: int
        :param turn: bool, in turn
        """
        print("Set turn to", uid, turn)
        for player in self.players:
            if player.get_uid() == uid:
                if turn:
                    player.set_active()
                else:
                    player.set_inactive()

    def set_name(self, uid, name):
        player = self.get_player(uid)
        player.set_name(name)

    def is_empty(self):
        return len(self.players) == 0

    def get_player(self, uid):
        for player in self.players:
            if player.get_uid() == uid:
                return player


class Player(Frame):

    def __init__(self, master, name, uid):
        super().__init__(master)
        self.name_label = Label(self, text=name, font=("Helvetica", 24))
        self.name_label.pack(fill="both")
        self.name = name
        self.uid = uid

    def __str__(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.name_label.config(text=self.name)

    def get_name(self):
        return self.name

    def get_uid(self):
        return self.uid

    def set_active(self):
        self.name_label.config(bg="#39B526")

    def set_inactive(self):
        self.name_label.config(bg="#B7B7B7")
