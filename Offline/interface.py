from game import Game


def create_players():
    """
    Creates players
    Only for offline version
    :return: list tuples (int, str)
    """
    players = []
    for index in range(int(input("How many players? >"))):
        name = "Player " + str(index)
        players.append((index, name))
    return players


if __name__ == "__main__":

    players = create_players()
    game = Game(players)

    while len(game.turnmanager.get_players()) > 1:
        pass