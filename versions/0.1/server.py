import socket                   # Import socket module
import json
from utilities import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
# host = "192.168.1.132"
print(host)
port = 12345                    # Reserve a port for your service.
server.bind((host, port))            # Bind to the port
server.listen()


class Game:

    def __init__(self):
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
            except:
                client.close()
                print(f"{self.clients[client]['address']} disconnected!")
                del (self.clients[client])
                break

    def receive(self):
        while True:
            client, address = server.accept()
            print(f"{str(address)} connected!")
            self.clients[client] = {"address": address}

            # Send start info
            info = {
                "player": {"add": ["2S", "10D", "QS"]},
                "opponent":
                    [
                        {"Juuso": {"amount": 10,
                                   "won": 0,
                                   "lost": 0}
                        },
                        {"Petteri": {"amount": 3,
                                     "won": 0,
                                     "lost": 0}
                        }
                    ],
                "deck": {"amount": 10,
                         "drawtop": "2D"},
                "game": {"latest": {"amount": 3,
                                    "rank": "J"},
                         "amount": 24,
                         "suspect": {"cards": ["8D, 9H"],
                                     "lied": 1}
                        },
                "sidebar": {"allowed": ["J", "Q", "K", "A", "2"],
                            "denied": ["3", "4", "5"]}

            }
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
    game = Game()