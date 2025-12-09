# option_page.py
import terminalio
from adafruit_display_text import label

class OptionPage:
    def __init__(self, group):
        self.group = group
        self.options = ["Easy", "Normal", "Hard", "Infinite"]
        self.descrips = ["  goal:20", "goal:20", "  goal:30", "-----"]
        self.refresh()

    def refresh(self):
        self.index = 0
        self.selected = False

        self.labels = [] 
        self.draw_static()
        self.update_arrow()

    def draw_static(self):
        title = label.Label(terminalio.FONT, text="Select Mode", x=10, y=5)
        self.group.append(title)
        
        for i, opt in enumerate(self.options):
            txt = label.Label(
                terminalio.FONT,
                text=f"  {opt}: {self.descrips[i]}", 
                x=20,
                y=18 + i * 12
            )
            self.group.append(txt)
            self.labels.append(txt)

    def update_arrow(self):
        for i, lbl in enumerate(self.labels):
            if i == self.index:
                lbl.text = f"> {self.options[i]}: {self.descrips[i]}"
            else:
                lbl.text = f"  {self.options[i]}: {self.descrips[i]}"

    def receive(self, msg):
        if msg == "UP":
            self.index = (self.index - 1) % len(self.options)
            self.update_arrow()

        elif msg == "DOWN":
            self.index = (self.index + 1) % len(self.options)
            self.update_arrow()

        elif msg == "PRESS":
            self.selected = True

    def get_result(self):
        if self.selected:
            return self.options[self.index]
        return None

    def clear_figure(self):
        while len(self.group) > 0:
            self.group.pop()
