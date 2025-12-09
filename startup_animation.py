import displayio
import vectorio
import time
from adafruit_display_text import label
import terminalio

class StartupAnimation:
    def __init__(self, main_group, width=128, height=64):
        self.width = width
        self.height = height
        self.main_group = main_group

        # 临时 group
        self.anim_group = displayio.Group()
        main_group.append(self.anim_group)

        # ---------- 扩展圆 ----------
        self.circle_palette = displayio.Palette(1)
        self.circle_palette[0] = 0xFFFFFF
        self.circle = vectorio.Circle(
            pixel_shader=self.circle_palette,
            radius=1,
            x=width // 2,
            y=height // 2
        )
        self.anim_group.append(self.circle)
        self.radius = 1

        # 标题文字先创建，不加到 group
        self.title = label.Label(
            terminalio.FONT,
            text="Flappy Ball",
            color=0x000000 if width > height else 0xFFFFFF  # 可根据背景调整
        )
        # 居中
        self.title.anchor_point = (0.5, 0.5)
        self.title.anchored_position = (width//2, height//2)

        self.running = True

    def update(self):
        if not self.running:
            return False

        # 最大半径，让圆填满屏幕对角线
        max_radius = int((self.width**2 + self.height**2)**0.5 / 2) + 2

        if self.radius < max_radius:
            self.radius += 2  # 扩展速度
            self.circle.radius = int(self.radius)
        else:
            # 圆扩展完成，显示文字
            if self.title not in self.anim_group:
                self.anim_group.append(self.title)
                # 等待 1 秒再结束动画
                time.sleep(3)
            self.running = False

        return self.running

    def play(self):
        self.running = True
        self.radius = 1
        while self.running:
            self.update()
            time.sleep(0.03)

        # 清理 group
        self.clear()

    def clear(self):
        while len(self.anim_group) > 0:
            self.anim_group.pop()
        self.main_group.remove(self.anim_group)
