from tkinter import *
from time import sleep
from threading import Thread


def find_ratio(a, s):
    """
    Return ratio of geometric sum
    :param a: float, first
    :param s: float, sum
    :return: float, ratio
    """
    return -((a / s) - 1)

class ClaimText(Label):
    """
    Claim shown as text
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.config(bg="#35654d", fg="white", text="No cards played", font=("", 12))

    def new(self, amount, rank):
        """
        Set new claim
        :param amount: int
        :param rank: str
        :return:
        """
        if amount == 0:
            self.reset()
            return
        self.config(text=f"Last claimed: {rank} x{amount}")

    def reset(self):
        """
        Reset the labels to default
        """
        self.config(text="No cards played")


class Claim(Frame):
    """
    Claim shown graphically
    """
    def __init__(self, parent):
        super().__init__(parent, bg="#35654d")
        self.parent = parent

        self.content = None

        self.placement = {
            1: lambda label, count: label.grid(),
            2: lambda label, count: label.grid(column=count, row=0),
            3: lambda label, count: label.grid(column=count % 2, row=int(count / 2), columnspan=1 if count <= 1 else 2),
            4: lambda label, count: label.grid(column=count % 2, row=int(count / 2)),
        }
        self.widgets = []
        self.start_interval = 2
        self.stop_interval = 0.15
        self.ratio = None
        self.flickering = False

    def new(self, amount, rank):

        self.reset()
        self.content = Frame(self, bg=self["bg"])
        self.content.pack(pady=50 if amount <= 2 else 0)

        for count in range(amount):
            label = Label(self.content, text=self.int_to_rank(rank), bg="white", font=("Helvetica", 36), width=2, height=2)
            self.placement[amount](label, count)
            label.grid_configure(padx=4, pady=4)
            self.widgets.append(label)

    def reset(self):
        if self.content:
            self.widgets = []
            self.content.destroy()

    def start_flicker(self, duration):
        self.flickering = True
        self.start_interval = duration * 0.1 if duration * 0.1 < self.start_interval else self.start_interval
        self.ratio = find_ratio(self.start_interval-self.stop_interval, duration)
        Thread(target=lambda: self.flicker(self.start_interval), daemon=True).start()

    def stop_flicker(self):
        self.flickering = False

    def flicker(self, interval):
        if not self.flickering:
            self.change_to_white()
            return
        if interval < self.stop_interval:
            self.change_to_white()
            return
        self.change_color()
        sleep(interval)
        self.flicker(interval * self.ratio)

    def change_color(self):
        for widget in self.widgets:
            if widget["bg"] == "white":
                widget.config(bg="red")
            else:
                widget.config(bg="white")

    def change_to_white(self):
        for widget in self.widgets:
            widget.config(bg="white")

    @staticmethod
    def int_to_rank(num):
        """
        Return rank according to given number
        :param num: int
        :return: str
        """

        ranks = {
            11: "J",
            12: "Q",
            13: "K",
            14: "A",
        }
        if num in ranks:
            return ranks[num]
        else:
            return str(num)
