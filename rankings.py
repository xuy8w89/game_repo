import displayio
import terminalio
import struct
from adafruit_display_text import label
import microcontroller
import gc

NVM_SIZE = 128

class Rankings:
    def __init__(self, group):
        self.group = group
        self.texts = []
        self.restart = False
        self.FORMAT = "3s3H"
        self.DATA_SIZE = struct.calcsize(self.FORMAT)
        self.records = [["A", 0], ["A", 0], ["A", 0]]
        self.load()


    def load(self):
        raw = bytes(microcontroller.nvm[:self.DATA_SIZE])
        chars, a, b, c = struct.unpack(self.FORMAT, raw)
        chars = chars.decode("ascii")
        for i, item in enumerate([a, b, c]):
            self.records[i][0] = chars[i]
            self.records[i][1] = item


    def save(self):
        chars = ""
        nums = []
        for item in self.records:
            chars += item[0]
            nums.append(item[1])
        a, b, c = nums
        packed = struct.pack(self.FORMAT, chars.encode("ascii"), a, b, c)
        for i in range(self.DATA_SIZE):
            microcontroller.nvm[i] = packed[i]

    def is_high_score(self, score):
        return score > self.records[-1][1]

    def insert(self, name, score):
        gc.collect() 
        self.records.append((name, score))
        self.records.sort(key=lambda x: x[1], reverse=True)
        self.records = self.records[:3]
        self.save()

    def show(self):
        self.texts.clear()

        title = label.Label(terminalio.FONT, text="RANKINGS", x=28, y=6)
        self.group.append(title)

        y = 18
        for i, (name, score) in enumerate(self.records):
            txt = f"{i+1}. {name}  {score}"
            t = label.Label(terminalio.FONT, text=txt, x=10, y=y)
            self.group.append(t)
            self.texts.append(t)
            y += 14

        helper = label.Label(
            terminalio.FONT,
            text="B2:Back  P:Clear",
            x=2, y=60
        )
        self.group.append(helper)

    def receive(self, event):
        if event == "PRESS":
            self.restart = True

        elif event == "CLEAR":
            self.records = [("A", 0), ("B", 0), ("C", 0)]
            self.save()
            self.clear_figure()
            self.show()

    def clear_figure(self):
        while len(self.group) > 0:
            self.group.pop()
        self.restart = False
