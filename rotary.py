import digitalio
import time

class Rotary:
    def __init__(self, pin_a, pin_b, pin_sw):
        self.a = digitalio.DigitalInOut(pin_a)
        self.b = digitalio.DigitalInOut(pin_b)
        self.sw = digitalio.DigitalInOut(pin_sw)

        for p in [self.a, self.b, self.sw]:
            p.direction = digitalio.Direction.INPUT
            p.pull = digitalio.Pull.UP   # 接 GND，必须上拉

        # 旋转状态
        self.last_a = self.a.value

        # 按钮状态
        self.last_sw = self.sw.value

        # 消抖时间
        self.last_rot_time = time.monotonic()
        self.last_sw_time = time.monotonic()

    def read(self):
        direction = 0
        pressed = False
        now = time.monotonic()

        # ---------- 旋转读取（10ms 消抖） ----------
        if now - self.last_rot_time > 0.01:
            self.last_rot_time = now
            a = self.a.value
            b = self.b.value

            if a != self.last_a:
                if b != a:
                    direction = 1   # 顺时针
                else:
                    direction = -1  # 逆时针
                self.last_a = a

        # ---------- 按键读取（20ms 消抖 + 边沿触发） ----------
        if now - self.last_sw_time > 0.02:
            self.last_sw_time = now
            sw = self.sw.value

            # 只在：从 松开 -> 按下 的瞬间触发
            if self.last_sw and not sw:
                pressed = True

            self.last_sw = sw

        return direction, pressed
