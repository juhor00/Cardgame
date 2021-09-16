"""
Client's main program
"""

import gui
import client


if __name__ == "__main__":
    gui = gui.Gui()
    client = client.Client(gui)
    gui.set_client(client)
    gui.start()
