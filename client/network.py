import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = "192.168.2.132"
        port = 12345
        self.addr = (server, port)
        self.id = int(self.connect())

        self.pending = []

    def get_id(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected")
            return self.client.recv(2048).decode()
        except:
            pass

    def disconnect(self):
        """
        Disconnect from the server
        """
        try:
            self.client.close()
            print("Disconnected")
        except socket.error:
            pass

    def get(self):
        """
        Get message from server
        :return: bytes
        """
        if self.pending:
            return self.pending.pop(0)
        try:
            message = self.client.recv(2048)
            packets = self.split_packets(message)
            if len(packets) == 1:
                return message

            # Pakcet splitting and pending
            pending = packets[1:]
            for packet in pending:
                self.pending.append(packet)
            return packets[0]
        except socket.error:
            print("An error occurred!")
            self.disconnect()
            return "disconnect"

    @staticmethod
    def split_packets(message):
        """
        Split different packets from the message and return a list of packets
        A packet is one dictionary
        :param message: bytes
        :return: list of bytes
        """
        open_brackets = 0
        open_index = 0
        packets = []

        for index, char in enumerate(message.decode(encoding="UTF-8")):
            if char == '{':
                if open_brackets == 0:
                    open_index = index
                open_brackets += 1
            if char == '}':
                open_brackets -= 1

                if open_brackets == 0:
                    packet = message[open_index:index+1]
                    packets.append(packet)
        return packets




    def send(self, data):
        """
        Send bytes data to server
        :param data: bytes
        """
        try:
            self.client.send(data)
        except socket.error as e:
            print(e)