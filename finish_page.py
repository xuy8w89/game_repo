import displayio
import terminalio
from adafruit_display_text import label

class FinishPage:
    def __init__(self, group):
        self.group = group
        self.restart = False

    def show(self, level_name):
        while len(self.group) > 0:
            self.group.pop()
        self.restart = False
        title_text = f"Level Complete!"
        title_label = label.Label(
            terminalio.FONT,
            text=title_text,
            x=5,
            y=10
        )
        self.group.append(title_label)

        level_label = label.Label(
            terminalio.FONT,
            text=f"Level: {level_name}",
            x=5,
            y=25
        )
        self.group.append(level_label)
        
        hint_label = label.Label(
            terminalio.FONT,
            text="Press button restart",
            x=5,
            y=55
        )
        self.group.append(hint_label)

    def receive(self, msg):
        if msg == "PRESS":
            self.restart = True
            
    def clear_figure(self):
        while len(self.group) > 0:
            self.group.pop()