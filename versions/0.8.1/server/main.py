import server as s
import game as g


def main():

    server = s.Server()
    game = g.CardGame(server)
    server.add_game(game)


if __name__ == "__main__":
    main()
