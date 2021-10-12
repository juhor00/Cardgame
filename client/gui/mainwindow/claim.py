from tkinter import *


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

        self.placement = {
            1: lambda label, count: label.grid(),
            2: lambda label, count: label.grid(column=count, row=0),
            3: lambda label, count: label.grid(column=count % 2, row=int(count / 2), columnspan=1 if count <= 1 else 2),
            4: lambda label, count: label.grid(column=count % 2, row=int(count / 2)),
        }
        self.widgets = []

    def new(self, amount, rank):

        self.reset()

        for count in range(amount):
            label = Label(self, text=rank, bg="white", font=("Helvetica", 36), width=2, height=2)
            self.placement[amount](label, count)
            label.grid_configure(padx=4, pady=4)
            self.widgets.append(label)

    def reset(self):
        for widget in self.widgets:
            widget.grid_forget()
            del widget




if __name__ == '__main__':
    root = Tk()
    claim = Claim(root)
    claim.pack()
    claim.new(3, "A")
    root.mainloop()
