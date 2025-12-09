import displayio
import terminalio
from adafruit_display_text import label

class NewHighScorePage:
    def __init__(self, group):
        self.group = group
        self.bg = displayio.Group()
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.index = 0
        self.name = ""
        self.done = False

    def show(self):
        self.bg = displayio.Group()

        t1 = label.Label(terminalio.FONT, text="NEW HIGH SCORE!", x=4, y=16)
        t2 = label.Label(terminalio.FONT, text="Select Initial", x=10, y=30)
        self.char_label = label.Label(
            terminalio.FONT, text=self.letters[self.index], x=58, y=50
        )

        self.bg.append(t1)
        self.bg.append(t2)
        self.bg.append(self.char_label)
        self.group.append(self.bg)

    def receive(self, event):
        if event == "DOWN":  # 只用一个方向
            self.index = (self.index + 1) % len(self.letters)
            self.char_label.text = self.letters[self.index]

        elif event == "PRESS":
            self.name = self.letters[self.index]
            self.done = True

    def clear_figure(self):
        while len(self.group) > 0:
            self.group.pop()
        self.done = False
