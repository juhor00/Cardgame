import socket
import json
import threading


from eventhandler import EventHandler


def new_thread(target, daemon=True, args=()):
    thread = threading.Thread(target=target, args=args, daemon=daemon)
    thread.start()


class Server:

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "192.168.0.178"
        port = 12345
        self.server.bind((host, port))
        self.server.listen()
        self.id_count = 0
        print("Server is online")
        new_thread(self.receive, daemon=False)
        self.event = EventHandler(self)

    def receive(self):
        """
        New client connections
        """
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} connected!")
            self.id_count += 1
            new_thread(lambda: self.handle(client))
            client.send(bytes(str(self.id_count), encoding="UTF-8"))

            self.event.add(client, self.id_count)

    def handle(self, client):
        """
        Handle connected client
        :param client: socket
        """
        while True:
            try:
                message = json.loads(client.recv(2048).decode())
                self.event.new(client, message)
            except socket.error:
                # Disconnect
                user = self.event.remove(client)
                client.close()
                print(f"{user} [{user.get_uid()}] disconnected!")
                self.id_count -= 1
                self.event.broadcast_lobby()
                self.event.broadcast_game()
                return

    @staticmethod
    def send(client, data):
        """
        Send data to client
        :param client: socket client
        :param data: dict
        """
        client.send(json.dumps(data).encode("UTF-8"))



if __name__ == '__main__':
    server = Server()