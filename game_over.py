# game_over.py
import displayio
import terminalio
from adafruit_display_text import label

class GameOverPage:
    def __init__(self, group):
        self.group = group
        self.restart = False

    def show(self, score):
        while len(self.group) > 0:
            self.group.pop()
        self.restart = False

        t1 = label.Label(terminalio.FONT, text="GAME OVER", x=20, y=20)
        t2 = label.Label(terminalio.FONT, text=f"Score: {score}", x=20, y=35)
        t3 = label.Label(terminalio.FONT, text="Press to Restart", x=5, y=55)

        self.group.append(t1)
        self.group.append(t2)
        self.group.append(t3)

    def receive(self, msg):
        if msg == "PRESS":
            self.restart = True

    def clear_figure(self):
        while len(self.group) > 0:
            self.group.pop()
