# Cardgame


ABOUT...

Note: this program is NOT ready yet and is in development.


This is an online multiplayer cardgame to play with friends. The game is 'Valepaska' (similar to shithead?).

I've been developing a server-client based cardgame with graphical UI.
I started this project to develop my own skills and have a fun game to play with friends online.
I've learned about server-client networking, multithreading and creating a user interface.

The whole project is written in Python.
Networking is done by using sockets and sending JSON packets over the network.
UI is done with tkinter, which was a bit problematic because it's not quite efficient for sudden changes in the interface.
I've been thinking about creating the client side with different programming language and different technology for the UI.


INSTRUCTIONS TO INSTALL AND RUN


There are client-folder and server-folder in the repository.

Server:
Server needs to be configured by setting the host (IP address) and port in server.py (this will be made with a separate file later)
Make sure you have forwarded the port in your router for this to work!
After that the server can be started by running server.py. If all goes well, you should get a print "Server is online" in the console.

Client:
You need to set the target host (IP address) and port in network.py. No port forwarding required for the client.
After that you can run the client by running client.py. If all goes well, you should see a lobby-view without any error prompts.
The game requires at least 2 player to join.


HOW TO USE

At least 2 clients must be connected to same server. After all set their usernames and click on "Ready" the game will start.
I will not go through the rules here, only some functionalities.
You can select up to 4 cards from your hand when it's your turn. (Selected  cards are shown in the middle of the screen. Your turn is shown at left bottom corner).
After you have selected the cards you need to claim the cards by selecting a card rank on the right bottom corner.
You can suspect other players' claims by clicking the game deck in the middle of the screen (when there are cards played).
You can navigate through your cards by scrolling or clicking the arrows when you have many cards.

As said, the game is still in development and some features are missing and the game is not fully playable yet. For instance, the ending is yet to be developed.
