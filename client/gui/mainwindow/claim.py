from tkinter import *


class Claim(Label):
    """
    Frame to show info about claimed cards
    Amount and claimed rank
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
        self.config(text=f"Last claimed: {rank} x{amount}")

    def reset(self):
        """
        Reset the labels to default
        """
        self.config(text="No cards played")


if __name__ == '__main__':
    root = Tk()
    claim = Claim(root)
    claim.pack()
    claim.new(3, "J")
    root.mainloop()
