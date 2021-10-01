from tkinter import *

try:
    from .card import OpenedCard
except ImportError:
    from card import OpenedCard


class ClaimGrid(Frame):

    def __init__(self, master):
        super().__init__(master, bg="#35654d")
        self.buttons = []
        self.create_buttons()

    def on_click(self, button: Button):
        """
        Creates a virtual signal
        :param button: Button
        """
        rank = OpenedCard.rank_to_int(button["text"])
        self.event_generate("<<Button-clicked>>", data={"content": rank})

    def create_buttons(self):
        """
        Creates the buttons to grid
        """
        width = 50
        height = 50
        buttons = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        for index, rank in enumerate(buttons):
            frame = Frame(self, width=width, height=height)
            frame.propagate(False)

            if index < 5:
                row = 0
                column = index
            elif index < 9:
                row = 1
                column = index - 5
            else:
                row = 2
                column = index - 9

            frame.grid(row=row, column=column, sticky="nsew")
            button = Button(frame, text=rank, bg="grey", fg="white")
            button.config(command=lambda param=button: self.on_click(param))
            button.pack(expand=True, fill=BOTH)
            self.buttons.append(button)

    def disable_buttons(self, buttons):
        """
        Disables given buttons
        :param buttons: list of str
        """
        for button_text in buttons:
            for button in self.buttons:
                button_rank = OpenedCard.rank_to_int(button["text"])
                if button_text == button_rank:
                    button.config(state="disabled")
                    break

    def enable_buttons(self, buttons):
        """
        Enables given buttons
        :param buttons: list of str
        """
        for button_text in buttons:
            for button in self.buttons:
                button_rank = OpenedCard.rank_to_int(button["text"])
                if button_text == button_rank:
                    button.config(state="normal")
                    break


if __name__ == "__main__":
    root = Tk()
    grid = ClaimGrid(root)
    grid.pack()
    root.mainloop()
