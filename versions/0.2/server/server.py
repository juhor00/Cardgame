import socket                   # Import socket module
import json
from utilities import *
import defaultcomms


class Server:

    def __init__(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        # host = "192.168.1.132"
        port = 12345
        self.server.bind((host, port))
        self.server.listen()

        print("Server is online")
        self.clients = {}
        new_thread(self.receive, daemon=False)

    def __del__(self):
        print("Server shut down")

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024).decode("UTF-8")
                print("Server: ", message)
            except socket.error:
                client.close()
                print(f"{self.clients[client]['address']} disconnected!")
                del (self.clients[client])
                break

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"{str(address)} connected!")
            self.clients[client] = {"address": address}

            # Send start info
            info = defaultcomms.game_init_info
            json_obj = json.dumps(info)
            byte_obj = bytes(json_obj, encoding="UTF-8")
            client.send(byte_obj)

            thread = threading.Thread(target=lambda: self.handle(client))
            thread.start()

    @staticmethod
    def send_dict(info, client):
        """
        Sends a dictionary
        :param info: dict
        :param client: socket client
        """
        json_obj = json.dumps(info)
        byte_obj = bytes(json_obj, encoding="UTF-8")
        client.send(byte_obj)


if __name__ == "__main__":
    server = Server()
