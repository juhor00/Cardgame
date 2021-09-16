from tkinter import *


class TurnList(Frame):

    def __init__(self, master):
        super().__init__(master, bg="#35654d")

        self.players = []

    def add_players(self, list_of_players):
        """
        Adds players to turn list
        :param list_of_players: list of str, "You" must be included
        """
        # Clear old list
        for widget in self.winfo_children():
            if type(widget) == Player:
                widget.grid_forget()

        # You on top
        while list_of_players[0] != "You":
            list_of_players = [list_of_players[-1]] + list_of_players[:-1]

        # Grid players
        max_len = 0
        for name in list_of_players:
            if len(name) > max_len:
                max_len = len(name)
            player = Player(self, name)
            player.grid(sticky="nsew")
            self.players.append(player)

        self.update()
        for widget in self.winfo_children():
            if type(widget) == Player:
                widget.config(width=max_len)

    def set_turn(self, name):
        """
        Mark player active
        :param name: str
        """
        for player in self.players:
            if str(player) == name:
                player.set_active()
            else:
                player.set_inactive()

    def is_empty(self):
        return len(self.players) == 0


class Player(Frame):

    def __init__(self, master, name):
        super().__init__(master)
        self.name_label = Label(self, text=name, font=("Helvetica", 24))
        self.name_label.pack(fill="both")
        self.name = name

    def __str__(self):
        return self.name

    def set_active(self):
        self.name_label.config(bg="#39B526")

    def set_inactive(self):
        self.name_label.config(bg="#B7B7B7")


if __name__ == "__main__":
    root = Tk()
    turnlist = TurnList(root)
    turnlist.pack()
    turnlist.add_players(["Perkele", "Saatana", "You"])
    turnlist.set_turn("Saatana")
    root.mainloop()