"""
A module to handle turns and players
"""


from player import Player

PLAYER_AMOUNT = 4


class TurnManager:

    def __init__(self):

        self.turnlist = []
        self.turn = 0
        self.allowed_to_change = True
        self.active_player = None
        self.players = {}
        self.create_players()
        self.active_player = self.turnlist[self.turn]

    def stay_next_turn(self):
        """
        Stay on the same player next round
        """
        self.allowed_to_change = False

    def force_next_turn(self):
        """
        Forces the turn to change
        """
        self.allowed_to_change = True

    def change_turn(self):
        """
        Changes the turn
        """
        if not self.allowed_to_change:
            self.allowed_to_change = True
            return
        
        self.turn += 1
        if self.turn >= len(self.turnlist):
            self.turn = 0
        self.active_player = self.turnlist[self.turn]

    def create_players(self):
        """
        Creates players
        Only for offline version
        """
        for index in range(PLAYER_AMOUNT):
            name = "Player "+str(index)
            self.players[name] = Player(name)
            self.turnlist.append(self.players[name])

    def get_players(self):
        """
        Return list of all players
        :return: list, Player
        """
        players = []
        for name in self.players:
            players.append(self.players[name])

        return players

    def get_names(self):
        """
        Return list of all player names
        :return: list, str
        """

        names = []
        for name in self.players:
            names.append(name)

        return sorted(names)

    def get_player(self, name):
        """
        Get player by name
        :param name: str
        """
        if name not in self.get_names():
            return None

        return self.players[name]

    def get_active_player(self):
        """
        Return active player
        :return: Player
        """
        return self.active_player

    def remove_active(self):
        """
        Removes the active player
        """
        self.turnlist.remove(self.active_player)
        name = str(self.active_player)
        del(self.players[name])
        self.allowed_to_change = True

    def turn_to(self, name):
        """
        Change turn to a specific player
        :param name: str
        """
        if name not in self.get_names():
            return
        while name != self.active_player.name:
            self.change_turn()

    def print(self):
        """
        Prints all players
        """
        print("Players: ")
        for name in self.get_names():
            print(f"  {name}")

    def print_others(self):
        """
        Prints all active player's opponents
        """
        print("Players: ")
        for name in self.get_names():
            if name is not self.active_player.name:
                print(f"  {name}")
