"""
A module to handle turns and players
"""


from player import Player

PLAYER_AMOUNT = 4


class TurnManager:

    def __init__(self, players):

        self.turnlist = players
        self.turn = 0
        self.allowed_to_change = True
        self.active_player = None
        self.players = self.create_players_dict(players)
        self.active_player = self.turnlist[self.turn]

    @staticmethod
    def create_players_dict(players):
        """
        Create a dictionary of players based on their id's
        :param players: list of Players
        :return: dict, id : Player
        """
        players_by_id = {}
        for player in players:
            player_id = player.get_id()
            players_by_id[player_id] = player
        return players_by_id

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

    def get_players(self):
        """
        Return list of all players
        :return: list, Player
        """
        players = []
        for player_id in self.players:
            players.append(self.players[player_id])

        return players

    def get_names(self):
        """
        Return list of all player names
        :return: list, str
        """

        names = []
        for player_id in self.players:
            name = self.players[player_id].get_name()
            names.append(name)

        return sorted(names)

    def get_player(self, name):
        """
        Get player by name
        :param name: Player
        """
        for player_id in self.players:
            player = self.players[player_id]
            if player.get_name() == name:
                return player
        return None

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
        player_id = self.active_player.get_id()
        del(self.players[player_id])
        self.allowed_to_change = True

    def turn_to(self, name):
        """
        Change turn to a specific player
        :param name: str
        """
        if name not in self.get_names():
            return
        while name != self.active_player.get_name():
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
            if name is not self.active_player.get_name():
                print(f"  {name}")
