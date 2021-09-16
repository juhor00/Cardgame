from tkinter import Frame, Button, Entry, StringVar, Label


class Lobby(Frame):

    def __init__(self, master, width, height):
        width = int(width)
        height = int(height)
        super().__init__(master, width=width, height=height)

        self.opponents = {}

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

    def add_opponent(self, name):
        """
        Adds a new opponent
        :param name: str
        """
        self.update()
        height = self.others.winfo_height() / 5 - 30
        opponent = Opponent(self.others, name, height)
        opponent.place(x=0, y=(height+30)*len(self.opponents))
        opponent.update()
        self.opponents[name] = opponent

    def remove_all(self):
        print("Before", self.opponents)
        for name in self.opponents:
            opponent = self.opponents[name]
            opponent.place_forget()
        self.opponents = {}
        print("After", self.opponents)

    def remove_opponent(self, name):
        """
        Removes an opponent
        :param name: str
        """
        del self.opponents[name]

    def set_state(self, name, state):
        """
        Set state to an opponent
        :param name: str
        :param state: bool
        """
        opponent = self.opponents[name]
        self.opponents[name].set_state(state)

    def get_name(self):
        return self.entry.get()


class Opponent(Frame):
    def __init__(self, master: Frame, name: str, height):
        super().__init__(master)
        master.update()
        width = master.winfo_width()
        self.config(width=width, height=height, bg="grey")
        self.label = Label(self, text=name, bg="lightgrey", font=("Helvetica", 32))
        self.label.place(x=0, y=0, width=width-height-30, height=height)
        self.label.update()
        self.image = Label(self, bg="red")
        self.image.place(x=self.label.winfo_width()+30, y=0, width=height, height=height)
        self.ready = False

    def set_state(self, state):
        """
        Set opponent's state to ready or not ready
        :param state: bool
        """
        if self.ready:
            if state:
                return
            self.image.config(bg="red")
            self.ready = False

        else:
            if not state:
                return
            self.image.config(bg="green")
            self.ready = True

