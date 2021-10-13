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

    def on_click(self, button: 'ClaimButton'):
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
            reason = buttons[rank]
            rank = int(rank)
            button = self.get_button(rank)
            button.set_reason(reason)
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
        """
        Return button with given rank
        :param rank: int
        :return: ClaimButton
        """
        for button in self.buttons:
            if button.get_rank() == rank:
                return button


class ClaimButton(Button):

    def __init__(self, master, rank):
        super().__init__(master=master, text=rank)

        self.rank = rank
        self.reason = None

        self.enabled = False

        self.reasons = {
            0: None,
            1: "10 or Ace can't be played when there are no played cards",
            2: "Can't play court cards before deck is empty",
            3: "Can't play rank that is less than already played",
            4: "Only 2 can be played on top of 2",
            5: "10 can only be played if last played is 9 or lower",
            6: "Ace can only be played if last played is Jack or higher",
            7: "Court cards can only be played if last played is 7 or higher",
            8: "Not allowed when it is not your turn",
            9: "2, 10 or Ace can't be played when over 1 card is selected"
            }

        self.popup = ToolTip(self)
        self.bind("<Enter>", lambda event: self.popup.showtip(self.get_reason()) if not self.is_enabled() else None)
        self.bind("<Leave>", lambda event: self.popup.hidetip() if not self.is_enabled() else None)

    def get_rank(self):
        return self.rank

    def enable(self):
        self.config(state="normal")
        self.enabled = True

    def disable(self):
        self.config(state="disabled")
        self.enabled = False

    def is_enabled(self):
        return self.enabled

    def set_reason(self, reason_id):
        """
        Set reason why button cannot be used
        :param reason_id: int
        """
        self.reason = self.reasons[reason_id]

    def get_reason(self):
        return self.reason


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0

    def showtip(self, text):
        """Display text in tooltip window"""
        if self.tipwindow or not text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
