from tkinter import *

MAX_EVENTS = 5


class EventList(Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=parent["bg"])
        self.parent = parent

        self.events = []

    def discard(self):
        """
        Add discard event
        """
        self.new("Deck was discarded")

    def won(self, name: str, placement: int):
        """
        Add player won event
        :param name: str
        :param placement: int
        """
        placements = {
            1: "1st",
            2: "2nd",
            3: "3rd",
        }
        if placement not in placements:
            placement_text = f"{placement}th"
        else:
            placement_text = placements[placement]

        text = f"{name} was {placement_text} to win!"
        self.new(text)

    def played_cards(self, name: str):
        """
        Add card play event
        :param name: str
        """
        self.new(f"{name} played")

    def played_deck(self, name: str):
        """
        Add deck play event
        :param name: str
        """
        self.new(f"{name} played from the deck")

    def suspected(self, name: str, won: bool):
        """
        Add suspect event
        :param name: str
        :param won: bool, won the suspect or not
        """
        self.new(f"{name} suspected and {'won' if won else 'lost'} the suspect")

    def new(self, text):
        event = Label(self, text=text, font=("Helvetica", 16), wraplength=250, justify="left")
        event.pack(side=BOTTOM, anchor="w")
        self.events.append(event)

        if len(self.events) > MAX_EVENTS:
            self.remove()

    def remove(self):
        event = self.events.pop(0)
        event.destroy()


if __name__ == '__main__':
    root = Tk()
    eventlist = EventList(root)
    eventlist.pack()

    eventlist.played_cards("Jussi")
    eventlist.discard()
    eventlist.played_cards("Juuso")
    eventlist.suspected("Jussi", True)
    eventlist.played_deck("Jussi")
    eventlist.discard()
    eventlist.won("Jussi", 1)

    root.mainloop()