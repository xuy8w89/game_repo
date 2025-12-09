import board
import digitalio
import time

button0 = digitalio.DigitalInOut(board.D0)
button1 = digitalio.DigitalInOut(board.D1)
button2 = digitalio.DigitalInOut(board.D2)
button0.direction = digitalio.Direction.INPUT
button0.pull = digitalio.Pull.UP   # ✅ 打开内部上拉
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP   # ✅ 打开内部上拉
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP   # ✅ 打开内部上拉
while True:
    if not button0.value:   # 按下 = False
        print("bt0")
    if not button1.value:   # 按下 = False
        print("bt1")
    if not button2.value:   # 按下 = False
        print("bt2")
    time.sleep(0.05)