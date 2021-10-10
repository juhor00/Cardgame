from tkinter import *

try:
    from .card import OpenedCard
except ImportError:
    from card import OpenedCard


class ClaimGrid(Frame):

    def __init__(self, master):
        super().__init__(master, bg="#35654d")
        self.buttons = []
        self.enabled = []
        self.disabled = []
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
            button = ClaimButton(frame, OpenedCard.rank_to_int(rank))
            button.config(bg="grey", fg="white", text=rank)
            button.config(command=lambda param=button: self.on_click(param))
            button.pack(expand=True, fill=BOTH)
            self.buttons.append(button)

    def disable_buttons(self, buttons, temp=False):
        """
        Disables given buttons
        :param buttons: list of str
        :param temp: bool, temporary disable
        """
        for rank in buttons:
            button = self.get_button(rank)
            button.disable()

            if not temp:
                if button in self.enabled:
                    self.enabled.remove(button)
            self.disabled.append(button)

    def enable_buttons(self, buttons, temp=False):
        """
        Enables given buttons
        :param buttons: list of str
        :param temp: bool, was temporarily disabled
        """

        for rank in buttons:
            button = self.get_button(rank)

            if temp:
                if button not in self.enabled:
                    continue

            button.enable()
            if button not in self.enabled:
                self.enabled.append(button)

    def get_button(self, rank):
        for button in self.buttons:
            if button.get_rank() == rank:
                return button


class ClaimButton(Button):

    def __init__(self, master, rank):
        super().__init__(master=master, text=rank)

        self.rank = rank

    def get_rank(self):
        return self.rank

    def enable(self):
        self.config(state="normal")

    def disable(self):
        self.config(state="disabled")
