from player import Player

class Lobby:

    def __init__(self):
        self.players = {}

    def start(self):
        pass

    def wait_for_start(self):
        pass

    def event(self, client, address, info):
        """
        Handle events
        :param client:
        :param address:
        :param info:
        :return:
        """

        if client not in self.players:
            player = Player(client, address)
            self.players[client] = player
        else:
            player = self.players[client]
        if "name" in info:
            name = info["name"]
            player.add_name(name)

        ready = bool(info["ready"])
        player.set_ready(ready)
        self.broadcast()
        self.check_start()

    def broadcast(self):
        """
        Broadcast lobby info
        """
        for send_client in self.players:
            opponents = []
            for other_client in self.players:
                if not other_client == send_client:
                    player = self.players[other_client]
                    name = player.get_name()
                    ready = int(player.is_ready())
                    opponents.append({"name": name, "ready": ready})
            opponents_info = {"opponents": opponents}
            lobby_info = {"lobby": opponents_info}
            self.server.send_dict(lobby_info, send_client)