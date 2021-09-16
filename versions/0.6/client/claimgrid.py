from tkinter import Frame, Button, BOTH


class ClaimGrid(Frame):

    def __init__(self, master, settings):
        super().__init__(master, bg=settings["green"])
        self.buttons = []
        self.settings = settings
        self.create_buttons()

    def on_click(self, button: Button):
        """
        Creates a virtual signal
        :param button: Button
        """
        print(button, button["text"])
        self.event_generate("<<Button-clicked>>", data={"content": button["text"]})

    def create_buttons(self):
        """
        Creates the buttons to grid
        """
        columns = int(self.settings["claimgrid_columns"])
        width = int(self.settings["claimgrid_width"])
        height = int(self.settings["claimgrid_height"])
        buttons = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]
        for index, rank in enumerate(buttons):
            frame = Frame(self, width=width, height=height)
            frame.propagate(False)
            frame.grid(row=int(index / columns), column=int(index % columns), sticky="nsew")
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
                print(button)
                if button_text == button["text"]:
                    button["state"] = "disabled"
                    break

    def enable_buttons(self, buttons):
        """
        Enables given buttons
        :param buttons: list of str
        """
        for button_text in buttons:
            for button in self.buttons:
                print(button)
                if button_text == button["text"]:
                    button["state"] = "normal"
                    break
