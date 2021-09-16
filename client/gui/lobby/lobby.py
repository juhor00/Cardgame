from tkinter import Frame, Button, Entry, StringVar, Label


class Lobby(Frame):

    def __init__(self, master, width, height):
        width = int(width)
        height = int(height)
        super().__init__(master, width=width, height=height)

        self.readybutton = Button(self, text="Ready", command=self.on_button_click,
                                  bg="green", fg="white", font=("Helvetica", 50))
        self.readybutton.place(x=30, y=550, width=250)
        self.readybutton.update()
        self.textvar = StringVar(self)
        self.entry = Entry(self, font=("Helvetica", 50), textvariable=self.textvar)
        self.entry.place(x=60+self.readybutton.winfo_width(), y=550,
                         width=width - self.readybutton.winfo_width() - 90,
                         height=self.readybutton.winfo_height())

        self.others = Frame(self, width=width - 60, height=height - self.readybutton.winfo_height() - 100, bg="grey")
        self.others.place(x=30, y=30)
        self.opponents = []

    def on_button_click(self):
        name = self.entry.get()
        if name == "":
            return
        if self.readybutton["text"] == "Ready":
            self.readybutton.config(text="Cancel", bg="red")
            self.event_generate("<<Ready>>")
        else:
            self.readybutton.config(text="Ready", bg="green")
            self.event_generate("<<Cancel>>")

    def add_opponent(self, name, ready):
        """
        Adds a new opponent
        :param name: str
        :param ready: bool
        """
        self.update()
        height = self.others.winfo_height() / 5 - 30
        opponent = Opponent(self.others, height, name, ready)
        opponent.place(x=0, y=(height+30)*len(self.opponents))
        opponent.update()
        self.opponents.append(opponent)

    def get_opponents(self):
        """
        Return list of opponents
        :return: [str]
        """
        opponents = []
        for player in self.opponents:
            name = player.get_name()
            opponents.append(name)
        return opponents

    def remove_all(self):
        for opponent in self.opponents:
            opponent.place_forget()
        self.opponents = []

    def get_name(self):
        return self.entry.get()


class Opponent(Frame):
    def __init__(self, master: Frame, height: int, name: str, ready: bool):
        super().__init__(master)
        self.name = name
        master.update()
        width = master.winfo_width()
        self.config(width=width, height=height, bg="grey")
        self.label = Label(self, text=name, bg="lightgrey", font=("Helvetica", 32))
        self.label.place(x=0, y=0, width=width-height-30, height=height)
        self.label.update()
        self.image = Label(self, bg="green" if ready else "red")
        self.image.place(x=self.label.winfo_width()+30, y=0, width=height, height=height)

    def get_name(self):
        """
        Return name
        :return: str
        """
        return self.name

